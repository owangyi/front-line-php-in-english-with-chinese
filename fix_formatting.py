#!/usr/bin/env python3
"""
Fix formatting issues in generated Markdown files
"""
import re
import os
import glob

def fix_hyphenated_words(text):
    """Fix hyphenated words split across lines"""
    # Fix words split with hyphen and newline
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Fix words split with space and newline (common in PDF extraction)
    text = re.sub(r'(\w+)\s+\n\s*(\w+)', r'\1 \2', text)
    return text

def fix_code_blocks(text):
    """Detect and format code blocks"""
    lines = text.split('\n')
    result = []
    in_code = False
    code_lines = []
    
    for i, line in enumerate(lines):
        # Detect code patterns
        is_code_line = (
            line.strip().startswith('$') or
            line.strip().startswith('<?php') or
            line.strip().startswith('<?=') or
            (line.strip().endswith(';') and not line.strip().startswith('#')) or
            (line.strip().endswith('{') or line.strip().endswith('}')) or
            (line.strip().startswith('//') and i > 0 and lines[i-1].strip().endswith(';')) or
            (re.match(r'^\s*(public|private|protected|function|class|interface|trait|namespace|use|return|if|else|foreach|while|for|switch|case|default|break|continue|try|catch|finally|throw|new|extends|implements)\s', line.strip()))
        )
        
        # Check if previous line was code
        prev_is_code = i > 0 and (
            lines[i-1].strip().startswith('$') or
            lines[i-1].strip().startswith('<?php') or
            lines[i-1].strip().endswith(';') or
            lines[i-1].strip().endswith('{') or
            lines[i-1].strip().endswith('}') or
            lines[i-1].strip().startswith('//')
        )
        
        if is_code_line or (in_code and (line.strip() == '' or prev_is_code)):
            if not in_code:
                # Start code block
                if result and result[-1].strip():
                    result.append('')
                result.append('```php')
                in_code = True
            code_lines.append(line)
        else:
            if in_code:
                # End code block
                if code_lines:
                    result.extend(code_lines)
                result.append('```')
                result.append('')
                code_lines = []
                in_code = False
            result.append(line)
    
    # Close any open code block
    if in_code:
        if code_lines:
            result.extend(code_lines)
        result.append('```')
    
    return '\n'.join(result)

def fix_paragraphs(text):
    """Fix paragraph spacing"""
    # Remove excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Ensure single blank line between paragraphs
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def fix_special_chars(text):
    """Fix special characters"""
    # Fix em dashes
    text = text.replace('—', '—')
    # Fix quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    return text

def process_file(file_path):
    """Process a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply fixes
    content = fix_hyphenated_words(content)
    content = fix_code_blocks(content)
    content = fix_paragraphs(content)
    content = fix_special_chars(content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {file_path}")

def main():
    # Find all markdown files
    md_files = []
    md_files.extend(glob.glob('*.md'))
    md_files.extend(glob.glob('**/*.md', recursive=True))
    
    for file_path in md_files:
        if 'extract_pdf' in file_path or 'process_chapters' in file_path or 'fix_formatting' in file_path:
            continue
        process_file(file_path)

if __name__ == "__main__":
    main()

