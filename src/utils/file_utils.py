"""
文件处理工具模块
处理文件上传、下载、预览等功能
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import mimetypes
from datetime import datetime


class FileManager:
    """文件管理器"""
    
    def __init__(self, base_path: str = "data/attachments"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, file_path: str, entity_type: str, entity_id: int) -> Dict[str, Any]:
        """保存文件到附件目录"""
        source_path = Path(file_path)
        if not source_path.exists():
            raise FileNotFoundError(f"源文件不存在: {file_path}")
        
        # 生成唯一文件名
        file_hash = self._generate_file_hash(source_path)
        file_ext = source_path.suffix
        new_filename = f"{file_hash}{file_ext}"
        
        # 创建目标目录
        target_dir = self.base_path / entity_type / str(entity_id)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制文件
        target_path = target_dir / new_filename
        shutil.copy2(source_path, target_path)
        
        # 获取文件信息
        file_info = {
            'filename': new_filename,
            'original_name': source_path.name,
            'file_path': str(target_path),
            'file_size': source_path.stat().st_size,
            'file_type': file_ext.lower(),
            'mime_type': mimetypes.guess_type(str(source_path))[0] or 'application/octet-stream'
        }
        
        return file_info
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
        except Exception:
            pass
        return False
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """获取文件信息"""
        path = Path(file_path)
        if not path.exists():
            return None
        
        stat = path.stat()
        return {
            'filename': path.name,
            'file_size': stat.st_size,
            'file_type': path.suffix.lower(),
            'mime_type': mimetypes.guess_type(str(path))[0] or 'application/octet-stream',
            'created_time': datetime.fromtimestamp(stat.st_ctime),
            'modified_time': datetime.fromtimestamp(stat.st_mtime)
        }
    
    def _generate_file_hash(self, file_path: Path) -> str:
        """生成文件哈希值"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def get_supported_formats(self) -> List[str]:
        """获取支持的文件格式"""
        return [
            # 图片格式
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
            # 文档格式
            '.pdf', '.doc', '.docx', '.txt', '.rtf',
            # 表格格式
            '.xls', '.xlsx', '.csv',
            # 演示文稿
            '.ppt', '.pptx',
            # 压缩格式
            '.zip', '.rar', '.7z',
            # 其他
            '.md', '.html', '.htm'
        ]
    
    def is_supported_format(self, file_path: str) -> bool:
        """检查文件格式是否支持"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.get_supported_formats()


class DocumentProcessor:
    """文档处理器"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf', '.doc', '.docx', '.txt', '.md']
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """提取文档中的文本内容"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self._extract_pdf_text(file_path)
        elif file_ext == '.docx':
            return self._extract_docx_text(file_path)
        elif file_ext == '.txt':
            return self._extract_txt_text(file_path)
        elif file_ext == '.md':
            return self._extract_md_text(file_path)
        else:
            return None
    
    def _extract_pdf_text(self, file_path: str) -> Optional[str]:
        """提取PDF文本"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            return "PDF处理需要安装PyPDF2库"
        except Exception as e:
            return f"PDF处理错误: {str(e)}"
    
    def _extract_docx_text(self, file_path: str) -> Optional[str]:
        """提取Word文档文本"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            return "Word文档处理需要安装python-docx库"
        except Exception as e:
            return f"Word文档处理错误: {str(e)}"
    
    def _extract_txt_text(self, file_path: str) -> Optional[str]:
        """提取纯文本文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    return file.read()
            except Exception:
                return "无法读取文本文件"
        except Exception as e:
            return f"文本文件处理错误: {str(e)}"
    
    def _extract_md_text(self, file_path: str) -> Optional[str]:
        """提取Markdown文件内容"""
        return self._extract_txt_text(file_path)


class ImageProcessor:
    """图片处理器"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    def get_image_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """获取图片信息"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'mode': img.mode,
                    'format': img.format,
                    'size': os.path.getsize(file_path)
                }
        except ImportError:
            return None
        except Exception:
            return None
    
    def create_thumbnail(self, file_path: str, thumb_path: str, size: tuple = (200, 200)) -> bool:
        """创建缩略图"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(thumb_path)
                return True
        except Exception:
            return False

