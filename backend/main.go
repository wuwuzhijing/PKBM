package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

// 数据结构
type KnowledgeItem struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Content     string    `json:"content"`
	Category    string    `json:"category"`
	Tags        string    `json:"tags"`
	CreatedDate time.Time `json:"created_date"`
	UpdatedDate time.Time `json:"updated_date"`
	FilePath    string    `json:"file_path"`
	FileType    string    `json:"file_type"`
}

type Category struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
}

type App struct {
	DB *sql.DB
}

// 数据库初始化
func (app *App) initDatabase() error {
	// 确保数据目录存在
	dataDir := "data"
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return err
	}

	// 尝试连接现有数据库，如果不存在则创建新的
	dbPath := filepath.Join(dataDir, "pkbm.db")
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return err
	}
	app.DB = db

	// 检查表是否存在
	var tableExists int
	err = db.QueryRow("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='knowledge_items'").Scan(&tableExists)
	if err != nil {
		return err
	}

	// 如果表不存在，创建表
	if tableExists == 0 {
		queries := []string{
			`CREATE TABLE IF NOT EXISTS knowledge_items (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				content TEXT,
				category TEXT,
				tags TEXT,
				created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
				updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
				file_path TEXT,
				file_type TEXT
			)`,
			`CREATE TABLE IF NOT EXISTS categories (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT UNIQUE NOT NULL,
				description TEXT
			)`,
		}

		for _, query := range queries {
			if _, err := db.Exec(query); err != nil {
				return err
			}
		}

		// 插入默认分类
		defaultCategories := []struct {
			name        string
			description string
		}{
			{"格言警句", "经典格言和警句"},
			{"方法论", "各种方法和理论"},
			{"技术文档", "技术相关的文档"},
			{"学习笔记", "学习过程中的笔记"},
			{"工作记录", "工作相关的记录"},
			{"生活感悟", "生活中的感悟和思考"},
			{"书籍摘要", "读书笔记和摘要"},
			{"其他", "其他类型的内容"},
		}

		for _, cat := range defaultCategories {
			_, err := db.Exec("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", cat.name, cat.description)
			if err != nil {
				log.Printf("插入分类失败: %v", err)
			}
		}

		log.Println("✓ 新数据库创建完成")
	} else {
		log.Println("✓ 连接现有数据库成功")
	}

	return nil
}

// 设置CORS
func enableCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}
		
		next.ServeHTTP(w, r)
	})
}

// 路由设置
func (app *App) setupRoutes() *mux.Router {
	r := mux.NewRouter()

	// API路由
	api := r.PathPrefix("/api").Subrouter()
	
	// 条目相关API
	api.HandleFunc("/items", app.getItems).Methods("GET")
	api.HandleFunc("/items", app.createItem).Methods("POST")
	api.HandleFunc("/items/{id:[0-9]+}", app.getItem).Methods("GET")
	api.HandleFunc("/items/{id:[0-9]+}", app.updateItem).Methods("PUT")
	api.HandleFunc("/items/{id:[0-9]+}", app.deleteItem).Methods("DELETE")
	
	// 分类相关API
	api.HandleFunc("/categories", app.getCategories).Methods("GET")
	api.HandleFunc("/categories", app.createCategory).Methods("POST")
	
	// 搜索API
	api.HandleFunc("/search", app.searchItems).Methods("GET")
	
	// 统计API
	api.HandleFunc("/stats", app.getStats).Methods("GET")

	return r
}

// API处理器
func (app *App) getItems(w http.ResponseWriter, r *http.Request) {
	rows, err := app.DB.Query(`
		SELECT id, title, content, category, tags, created_date, updated_date, file_path, file_type
		FROM knowledge_items 
		ORDER BY updated_date DESC
	`)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var items []KnowledgeItem
	for rows.Next() {
		var item KnowledgeItem
		rows.Scan(&item.ID, &item.Title, &item.Content, &item.Category, &item.Tags, 
			&item.CreatedDate, &item.UpdatedDate, &item.FilePath, &item.FileType)
		items = append(items, item)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(items)
}

func (app *App) getItem(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		http.Error(w, "无效的ID", http.StatusBadRequest)
		return
	}

	var item KnowledgeItem
	err = app.DB.QueryRow(`
		SELECT id, title, content, category, tags, created_date, updated_date, file_path, file_type
		FROM knowledge_items WHERE id = ?
	`, id).Scan(&item.ID, &item.Title, &item.Content, &item.Category, &item.Tags, 
		&item.CreatedDate, &item.UpdatedDate, &item.FilePath, &item.FileType)

	if err != nil {
		http.Error(w, "条目不存在", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(item)
}

func (app *App) createItem(w http.ResponseWriter, r *http.Request) {
	var item KnowledgeItem
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if item.Title == "" {
		http.Error(w, "标题不能为空", http.StatusBadRequest)
		return
	}

	result, err := app.DB.Exec(`
		INSERT INTO knowledge_items (title, content, category, tags, created_date, updated_date)
		VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
	`, item.Title, item.Content, item.Category, item.Tags)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	id, _ := result.LastInsertId()
	item.ID = int(id)
	item.CreatedDate = time.Now()
	item.UpdatedDate = time.Now()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(item)
}

func (app *App) updateItem(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		http.Error(w, "无效的ID", http.StatusBadRequest)
		return
	}

	var item KnowledgeItem
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	item.ID = id

	_, err = app.DB.Exec(`
		UPDATE knowledge_items 
		SET title = ?, content = ?, category = ?, tags = ?, updated_date = CURRENT_TIMESTAMP
		WHERE id = ?
	`, item.Title, item.Content, item.Category, item.Tags, id)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	item.UpdatedDate = time.Now()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(item)
}

func (app *App) deleteItem(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		http.Error(w, "无效的ID", http.StatusBadRequest)
		return
	}

	_, err = app.DB.Exec("DELETE FROM knowledge_items WHERE id = ?", id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func (app *App) getCategories(w http.ResponseWriter, r *http.Request) {
	rows, err := app.DB.Query("SELECT id, name, description FROM categories ORDER BY name")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var categories []Category
	for rows.Next() {
		var cat Category
		rows.Scan(&cat.ID, &cat.Name, &cat.Description)
		categories = append(categories, cat)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(categories)
}

func (app *App) createCategory(w http.ResponseWriter, r *http.Request) {
	var cat Category
	if err := json.NewDecoder(r.Body).Decode(&cat); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if cat.Name == "" {
		http.Error(w, "分类名不能为空", http.StatusBadRequest)
		return
	}

	// 检查是否已存在
	var exists int
	app.DB.QueryRow("SELECT COUNT(*) FROM categories WHERE name = ?", cat.Name).Scan(&exists)
	if exists > 0 {
		http.Error(w, "分类已存在", http.StatusBadRequest)
		return
	}

	result, err := app.DB.Exec("INSERT INTO categories (name, description) VALUES (?, ?)", cat.Name, cat.Description)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	id, _ := result.LastInsertId()
	cat.ID = int(id)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(cat)
}

func (app *App) searchItems(w http.ResponseWriter, r *http.Request) {
	query := strings.TrimSpace(r.URL.Query().Get("q"))
	if query == "" {
		http.Error(w, "搜索关键词不能为空", http.StatusBadRequest)
		return
	}

	rows, err := app.DB.Query(`
		SELECT id, title, content, category, tags, created_date, updated_date, file_path, file_type
		FROM knowledge_items 
		WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
		ORDER BY updated_date DESC
	`, "%"+query+"%", "%"+query+"%", "%"+query+"%")

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var items []KnowledgeItem
	for rows.Next() {
		var item KnowledgeItem
		rows.Scan(&item.ID, &item.Title, &item.Content, &item.Category, &item.Tags, 
			&item.CreatedDate, &item.UpdatedDate, &item.FilePath, &item.FileType)
		items = append(items, item)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(items)
}

func (app *App) getStats(w http.ResponseWriter, r *http.Request) {
	var totalItems, totalCategories int
	app.DB.QueryRow("SELECT COUNT(*) FROM knowledge_items").Scan(&totalItems)
	app.DB.QueryRow("SELECT COUNT(*) FROM categories").Scan(&totalCategories)

	stats := map[string]interface{}{
		"total_items":      totalItems,
		"total_categories": totalCategories,
		"server_time":      time.Now(),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(stats)
}

func main() {
	app := &App{}

	// 初始化数据库
	if err := app.initDatabase(); err != nil {
		log.Fatal("数据库初始化失败:", err)
	}
	defer app.DB.Close()

	// 设置路由
	router := app.setupRoutes()

	// 获取配置
	host := os.Getenv("PKBM_HOST")
	if host == "" {
		host = "127.0.0.1"
	}

	port := os.Getenv("PKBM_PORT")
	if port == "" {
		port = "8080"
	}

	// 启动服务器
	addr := host + ":" + port
	log.Printf("PKBM API服务器启动中...")
	log.Printf("API地址: http://%s/api", addr)
	log.Printf("按 Ctrl+C 停止服务器")

	// 启用CORS
	handler := enableCORS(router)

	if err := http.ListenAndServe(addr, handler); err != nil {
		log.Fatal("服务器启动失败:", err)
	}
}
