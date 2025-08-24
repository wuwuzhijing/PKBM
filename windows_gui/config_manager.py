#!/usr/bin/env python3
"""
配置管理模块
处理配置文件的读取、写入和验证
"""

import configparser
import os
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.default_config = self._get_default_config()
        self.load_config()
    
    def _get_default_config(self) -> Dict[str, Dict[str, Any]]:
        """获取默认配置"""
        return {
            'DATABASE': {
                'db_path': 'data/pkbm.db',
                'backup_dir': 'data/backups',
                'auto_backup_days': '7'
            },
            'INTERFACE': {
                'window_width': '1400',
                'window_height': '900',
                'theme': 'clam',
                'font_size': '10',
                'show_status_bar': 'true',
                'show_toolbar': 'true'
            },
            'CATEGORIES': {
                'default_color': '#3498db',
                'show_colors': 'true',
                'sort_by': 'name'
            },
            'SEARCH': {
                'history_count': '20',
                'fuzzy_search': 'true',
                'highlight_results': 'true'
            },
            'IMPORT': {
                'supported_extensions': '.txt,.md,.pb,.doc,.docx,.pdf',
                'max_file_size': '50',
                'auto_import': 'false',
                'default_import_category': '其他'
            },
            'EXPORT': {
                'export_format': 'md',
                'export_dir': 'exports',
                'include_metadata': 'true'
            },
            'BACKUP': {
                'auto_backup': 'true',
                'backup_retention_days': '30',
                'compress_backups': 'true'
            },
            'NETWORK': {
                'api_base_url': 'http://127.0.0.1:8080/api',
                'timeout': '30',
                'retry_count': '3'
            },
            'LOGGING': {
                'log_level': 'INFO',
                'log_file': 'logs/pkbm.log',
                'log_retention_days': '7',
                'console_output': 'true'
            },
            'SECURITY': {
                'encrypt_database': 'false',
                'hash_algorithm': 'sha256',
                'session_timeout': '60'
            },
            'UPDATES': {
                'check_updates': 'true',
                'update_server': 'https://api.github.com/repos/your-repo/releases/latest',
                'auto_download': 'false'
            }
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file, encoding='utf-8')
                print(f"✅ 配置文件加载成功: {self.config_file}")
                return True
            else:
                print(f"⚠️  配置文件不存在，创建默认配置: {self.config_file}")
                self.create_default_config()
                return True
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            return False
    
    def create_default_config(self) -> bool:
        """创建默认配置文件"""
        try:
            # 设置默认值
            for section, options in self.default_config.items():
                if not self.config.has_section(section):
                    self.config.add_section(section)
                
                for key, value in options.items():
                    self.config.set(section, key, str(value))
            
            # 保存配置文件
            self.save_config()
            print("✅ 默认配置文件创建成功")
            return True
            
        except Exception as e:
            print(f"❌ 创建默认配置文件失败: {e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            # 确保目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            
            print(f"✅ 配置文件保存成功: {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """获取配置值"""
        try:
            if self.config.has_section(section) and self.config.has_option(section, key):
                value = self.config.get(section, key)
                # 尝试转换为适当的数据类型
                return self._convert_value(value)
            else:
                # 返回默认值
                if section in self.default_config and key in self.default_config[section]:
                    return self._convert_value(self.default_config[section][key])
                return fallback
        except Exception as e:
            print(f"⚠️  获取配置值失败 [{section}][{key}]: {e}")
            return fallback
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """设置配置值"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            self.config.set(section, key, str(value))
            return True
            
        except Exception as e:
            print(f"❌ 设置配置值失败 [{section}][{key}]: {e}")
            return False
    
    def _convert_value(self, value: str) -> Any:
        """转换配置值类型"""
        # 布尔值
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # 整数
        try:
            if '.' not in value:
                return int(value)
        except ValueError:
            pass
        
        # 浮点数
        try:
            return float(value)
        except ValueError:
            pass
        
        # 字符串
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取整个配置段"""
        result = {}
        if self.config.has_section(section):
            for key in self.config.options(section):
                result[key] = self.get(section, key)
        return result
    
    def set_section(self, section: str, options: Dict[str, Any]) -> bool:
        """设置整个配置段"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            for key, value in options.items():
                self.config.set(section, key, str(value))
            
            return True
            
        except Exception as e:
            print(f"❌ 设置配置段失败 [{section}]: {e}")
            return False
    
    def has_section(self, section: str) -> bool:
        """检查配置段是否存在"""
        return self.config.has_section(section)
    
    def has_option(self, section: str, key: str) -> bool:
        """检查配置项是否存在"""
        return self.config.has_option(section, key)
    
    def remove_section(self, section: str) -> bool:
        """删除配置段"""
        try:
            return self.config.remove_section(section)
        except Exception as e:
            print(f"❌ 删除配置段失败 [{section}]: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """重置为默认配置"""
        try:
            self.config = configparser.ConfigParser()
            return self.create_default_config()
        except Exception as e:
            print(f"❌ 重置配置失败: {e}")
            return False
    
    def validate_config(self) -> bool:
        """验证配置文件"""
        try:
            # 检查必要的配置段
            required_sections = ['DATABASE', 'INTERFACE']
            for section in required_sections:
                if not self.has_section(section):
                    print(f"❌ 缺少必要的配置段: {section}")
                    return False
            
            # 检查数据库路径
            db_path = self.get('DATABASE', 'db_path')
            if not db_path:
                print("❌ 数据库路径配置错误")
                return False
            
            print("✅ 配置文件验证通过")
            return True
            
        except Exception as e:
            print(f"❌ 配置文件验证失败: {e}")
            return False

# 全局配置管理器实例
config_manager = ConfigManager()

def get_config(section: str, key: str, fallback: Any = None) -> Any:
    """获取配置值的便捷函数"""
    return config_manager.get(section, key, fallback)

def set_config(section: str, key: str, value: Any) -> bool:
    """设置配置值的便捷函数"""
    return config_manager.set(section, key, value)

def save_config() -> bool:
    """保存配置的便捷函数"""
    return config_manager.save_config()
