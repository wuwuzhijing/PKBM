"""
搜索工具模块
提供全文检索、标签搜索、分类搜索等功能
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime


class SearchEngine:
    """搜索引擎"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def global_search(self, query: str, limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """全局搜索，在所有类型的内容中搜索"""
        if not query.strip():
            return {}
        
        results = {
            'quotes': [],
            'abbreviations': [],
            'books': [],
            'total_count': 0
        }
        
        # 搜索格言与方法论
        from ..database.models import QuoteMethod
        quote_model = QuoteMethod(self.db_manager)
        quotes = quote_model.search(query, limit)
        results['quotes'] = quotes
        
        # 搜索科技名词缩写
        from ..database.models import TechAbbreviation
        abbr_model = TechAbbreviation(self.db_manager)
        abbreviations = abbr_model.search(query, limit)
        results['abbreviations'] = abbreviations
        
        # 搜索书籍
        from ..database.models import Book
        book_model = Book(self.db_manager)
        books = book_model.search(query, limit)
        results['books'] = books
        
        # 计算总数
        results['total_count'] = len(quotes) + len(abbreviations) + len(books)
        
        return results
    
    def advanced_search(self, query: str, filters: Dict[str, Any] = None, 
                       limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """高级搜索，支持过滤条件"""
        if not query.strip():
            return {}
        
        results = self.global_search(query, limit)
        
        if filters:
            # 应用标签过滤
            if 'tags' in filters and filters['tags']:
                results = self._filter_by_tags(results, filters['tags'])
            
            # 应用分类过滤
            if 'category' in filters and filters['category']:
                results = self._filter_by_category(results, filters['category'])
            
            # 应用时间过滤
            if 'date_range' in filters and filters['date_range']:
                results = self._filter_by_date_range(results, filters['date_range'])
            
            # 应用类型过滤
            if 'content_type' in filters and filters['content_type']:
                results = self._filter_by_content_type(results, filters['content_type'])
        
        return results
    
    def _filter_by_tags(self, results: Dict[str, List[Dict[str, Any]]], 
                        tags: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """按标签过滤结果"""
        filtered_results = {}
        
        for content_type, items in results.items():
            if content_type == 'total_count':
                continue
            
            filtered_items = []
            for item in items:
                item_tags = item.get('tags', [])
                if isinstance(item_tags, str):
                    try:
                        import json
                        item_tags = json.loads(item_tags)
                    except:
                        item_tags = []
                
                if any(tag in item_tags for tag in tags):
                    filtered_items.append(item)
            
            filtered_results[content_type] = filtered_items
        
        # 重新计算总数
        filtered_results['total_count'] = sum(
            len(items) for key, items in filtered_results.items() 
            if key != 'total_count'
        )
        
        return filtered_results
    
    def _filter_by_category(self, results: Dict[str, List[Dict[str, Any]]], 
                           category: str) -> Dict[str, List[Dict[str, Any]]]:
        """按分类过滤结果"""
        filtered_results = {}
        
        for content_type, items in results.items():
            if content_type == 'total_count':
                continue
            
            filtered_items = []
            for item in items:
                item_category = item.get('category', '')
                if category.lower() in item_category.lower():
                    filtered_items.append(item)
            
            filtered_results[content_type] = filtered_items
        
        # 重新计算总数
        filtered_results['total_count'] = sum(
            len(items) for key, items in filtered_results.items() 
            if key != 'total_count'
        )
        
        return filtered_results
    
    def _filter_by_date_range(self, results: Dict[str, List[Dict[str, Any]]], 
                             date_range: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """按时间范围过滤结果"""
        filtered_results = {}
        
        start_date = None
        end_date = None
        
        if 'start' in date_range:
            try:
                start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
            except:
                pass
        
        if 'end' in date_range:
            try:
                end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')
            except:
                pass
        
        for content_type, items in results.items():
            if content_type == 'total_count':
                continue
            
            filtered_items = []
            for item in items:
                item_date = item.get('created_at', '')
                if not item_date:
                    continue
                
                try:
                    if isinstance(item_date, str):
                        item_date = datetime.strptime(item_date, '%Y-%m-%d %H:%M:%S')
                    
                    if start_date and item_date < start_date:
                        continue
                    if end_date and item_date > end_date:
                        continue
                    
                    filtered_items.append(item)
                except:
                    continue
            
            filtered_results[content_type] = filtered_items
        
        # 重新计算总数
        filtered_results['total_count'] = sum(
            len(items) for key, items in filtered_results.items() 
            if key != 'total_count'
        )
        
        return filtered_results
    
    def _filter_by_content_type(self, results: Dict[str, List[Dict[str, Any]]], 
                               content_types: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """按内容类型过滤结果"""
        filtered_results = {}
        
        for content_type in content_types:
            if content_type in results:
                filtered_results[content_type] = results[content_type]
        
        # 重新计算总数
        filtered_results['total_count'] = sum(
            len(items) for key, items in filtered_results.items() 
            if key != 'total_count'
        )
        
        return filtered_results
    
    def search_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """搜索建议，基于搜索历史"""
        if not query.strip():
            return []
        
        from ..database.models import SearchHistory
        history_model = SearchHistory(self.db_manager)
        recent_searches = history_model.get_recent(50)
        
        suggestions = []
        query_lower = query.lower()
        
        for search in recent_searches:
            if query_lower in search.lower() and search not in suggestions:
                suggestions.append(search)
                if len(suggestions) >= limit:
                    break
        
        return suggestions
    
    def highlight_search_terms(self, text: str, query: str) -> str:
        """高亮搜索关键词"""
        if not query.strip() or not text:
            return text
        
        # 分割查询词
        terms = re.split(r'\s+', query.strip())
        
        # 高亮每个关键词
        highlighted_text = text
        for term in terms:
            if term:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                highlighted_text = pattern.sub(
                    f'<span style="background-color: yellow; font-weight: bold;">{term}</span>',
                    highlighted_text
                )
        
        return highlighted_text


class SearchIndexer:
    """搜索索引器"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def build_index(self):
        """构建搜索索引"""
        # 这里可以实现更复杂的索引构建逻辑
        # 目前使用简单的数据库索引
        pass
    
    def update_index(self, entity_type: str, entity_id: int):
        """更新特定实体的索引"""
        # 更新特定实体的搜索索引
        pass
    
    def remove_from_index(self, entity_type: str, entity_id: int):
        """从索引中移除实体"""
        # 从搜索索引中移除实体
        pass


class SearchAnalytics:
    """搜索分析"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取热门搜索"""
        from ..database.models import SearchHistory
        history_model = SearchHistory(self.db_manager)
        
        # 这里可以实现更复杂的统计逻辑
        # 目前返回最近的搜索记录
        recent_searches = history_model.get_recent(limit)
        
        return [{'query': query, 'count': 1} for query in recent_searches]
    
    def get_search_trends(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取搜索趋势"""
        # 实现搜索趋势分析
        return []
    
    def get_search_insights(self) -> Dict[str, Any]:
        """获取搜索洞察"""
        return {
            'total_searches': 0,
            'unique_users': 0,
            'popular_categories': [],
            'search_success_rate': 0.0
        }

