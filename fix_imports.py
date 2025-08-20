#!/usr/bin/env python3
"""
修复PyQt6导入问题的脚本
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """修复文件中的导入问题"""
    print(f"正在修复文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复QAction导入问题
        # 将QAction从QtWidgets移到QtGui
        content = re.sub(
            r'from PyQt6\.QtWidgets import \(([^)]*QAction[^)]*)\)',
            lambda m: fix_qaction_import(m.group(1)),
            content
        )
        
        # 修复Qt.Orientation问题
        content = content.replace('Qt.Orientation.Horizontal', 'Qt.Horizontal')
        content = content.replace('Qt.Orientation.Vertical', 'Qt.Vertical')
        
        # 修复Qt.Weight问题
        content = content.replace('QFont.Weight.Bold', 'QFont.Bold')
        content = content.replace('QFont.Weight.Normal', 'QFont.Normal')
        
        # 修复Qt.Shape问题
        content = content.replace('QFrame.Shape.StyledPanel', 'QFrame.StyledPanel')
        content = content.replace('QFrame.Shape.Box', 'QFrame.Box')
        content = content.replace('QFrame.Shape.Panel', 'QFrame.Panel')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已修复: {file_path}")
            return True
        else:
            print(f"- 无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ 修复失败: {file_path} - {e}")
        return False

def fix_qaction_import(import_line):
    """修复QAction的导入"""
    # 移除QAction
    import_line = re.sub(r',\s*QAction', '', import_line)
    import_line = re.sub(r'QAction\s*,?\s*', '', import_line)
    
    # 清理多余的逗号
    import_line = re.sub(r',\s*,', ',', import_line)
    import_line = re.sub(r'\(\s*,', '(', import_line)
    import_line = re.sub(r',\s*\)', ')', import_line)
    
    return import_line

def add_qaction_to_qtgui(file_path):
    """在QtGui导入中添加QAction"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有QAction在QtGui中
        if 'from PyQt6.QtGui import' in content and 'QAction' not in content:
            # 在QtGui导入中添加QAction
            content = re.sub(
                r'from PyQt6\.QtGui import ([^)]+)',
                r'from PyQt6.QtGui import \1, QAction',
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已在QtGui中添加QAction: {file_path}")
            return True
            
    except Exception as e:
        print(f"✗ 添加QAction失败: {file_path} - {e}")
        return False
    
    return False

def main():
    """主函数"""
    print("PKBM - PyQt6导入修复脚本")
    print("=" * 40)
    
    # 查找所有Python文件
    src_dir = Path("src")
    python_files = []
    
    if src_dir.exists():
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
    
    if not python_files:
        print("未找到Python文件")
        return
    
    print(f"找到 {len(python_files)} 个Python文件")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_imports_in_file(file_path):
            fixed_count += 1
        
        # 尝试添加QAction到QtGui导入
        add_qaction_to_qtgui(file_path)
    
    print(f"\n修复完成！共修复了 {fixed_count} 个文件")
    print("现在可以尝试运行程序了")

if __name__ == "__main__":
    main()
