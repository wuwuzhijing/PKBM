#!/usr/bin/env python3
"""
修复main.py的缩进问题
"""

def fix_indentation():
    """修复缩进问题"""
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        in_method = False
        method_indent = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                fixed_lines.append(line)
                continue
            
            # 检测方法定义
            if stripped.startswith('def ') and 'self' in stripped:
                in_method = True
                method_indent = 4
                fixed_lines.append(line)
                continue
            
            # 检测类定义结束
            if stripped == 'class PKBMImprovedGUI:' or stripped.startswith('class '):
                in_method = False
                method_indent = 0
                fixed_lines.append(line)
                continue
            
            # 修复缩进
            if in_method and stripped:
                # 计算正确的缩进
                if stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('else:') or stripped.startswith('for ') or stripped.startswith('while ') or stripped.startswith('try:') or stripped.startswith('except ') or stripped.startswith('finally:'):
                    # 控制语句，增加缩进
                    current_indent = method_indent + 4
                elif stripped.startswith('return') or stripped.startswith('break') or stripped.startswith('continue') or stripped.startswith('pass'):
                    # 简单语句，保持当前缩进
                    current_indent = method_indent + 4
                elif stripped.startswith('self.') or stripped.startswith('conn.') or stripped.execute('') or stripped.startswith('cursor.') or stripped.startswith('messagebox.') or stripped.startswith('ttk.') or stripped.startswith('tk.') or stripped.startswith('print(') or stripped.startswith('import ') or stripped.startswith('from '):
                    # 方法调用或语句，增加缩进
                    current_indent = method_indent + 4
                else:
                    # 其他情况，保持当前缩进
                    current_indent = method_indent + 4
                
                # 应用缩进
                fixed_line = ' ' * current_indent + stripped + '\n'
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        
        # 写回文件
        with open('main.py', 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("✅ 缩进修复完成")
        return True
        
    except Exception as e:
        print(f"❌ 修复缩进失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 修复main.py缩进问题...")
    if fix_indentation():
        print("🎉 缩进修复成功！")
    else:
        print("❌ 缩进修复失败！")
