"""
基本功能测试
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import unittest
from database.models import DatabaseManager
from utils.file_utils import FileManager
from utils.search_utils import SearchEngine


class TestDatabaseManager(unittest.TestCase):
    """测试数据库管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_db_path = "test_pkbm.db"
        self.db_manager = DatabaseManager(self.test_db_path)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_database_creation(self):
        """测试数据库创建"""
        self.assertTrue(os.path.exists(self.test_db_path))
    
    def test_connection(self):
        """测试数据库连接"""
        conn = self.db_manager.get_connection()
        self.assertIsNotNone(conn)
        conn.close()


class TestFileManager(unittest.TestCase):
    """测试文件管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = "test_attachments"
        self.file_manager = FileManager(self.test_dir)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_directory_creation(self):
        """测试目录创建"""
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_supported_formats(self):
        """测试支持的文件格式"""
        formats = self.file_manager.get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('.pdf', formats)
        self.assertIn('.jpg', formats)


class TestSearchEngine(unittest.TestCase):
    """测试搜索引擎"""
    
    def setUp(self):
        """测试前准备"""
        self.test_db_path = "test_search.db"
        self.db_manager = DatabaseManager(self.test_db_path)
        self.search_engine = SearchEngine(self.db_manager)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_search_engine_creation(self):
        """测试搜索引擎创建"""
        self.assertIsNotNone(self.search_engine)
    
    def test_global_search_empty_query(self):
        """测试空查询搜索"""
        results = self.search_engine.global_search("")
        self.assertEqual(results, {})


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestDatabaseManager))
    test_suite.addTest(unittest.makeSuite(TestFileManager))
    test_suite.addTest(unittest.makeSuite(TestSearchEngine))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("运行PKBM基本功能测试...")
    success = run_tests()
    
    if success:
        print("\n所有测试通过！")
        sys.exit(0)
    else:
        print("\n部分测试失败！")
        sys.exit(1)

