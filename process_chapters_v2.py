#!/usr/bin/env python3
"""
Process extracted PDF text and split into chapters - improved version
"""
import re
import os

def clean_text(text):
    """Clean extracted text"""
    # Remove page numbers (standalone numbers)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    # Remove "Front Line PHP" footer text
    text = re.sub(r'\s*\d+\s+Front Line PHP\s*', '', text, flags=re.MULTILINE)
    # Remove "Chapter XX - Title XX" page headers
    text = re.sub(r'^Chapter\s+\d+\s*-\s*[^\n]+\s+\d+\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    # Fix hyphenated words at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Fix spacing around code blocks
    text = re.sub(r'\n\s*([`$])', r'\n\1', text)
    return text.strip()

def find_chapter_boundaries(lines):
    """Find chapter boundaries in the text - only match CHAPTER XX (uppercase)"""
    boundaries = []
    current_chapter = None
    current_start = 0
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Match only "CHAPTER XX" (uppercase) - not "Chapter XX - Title"
        if re.match(r'^CHAPTER\s+\d+', line_stripped):
            if current_chapter:
                boundaries.append((current_chapter, current_start, i))
            chapter_num = re.search(r'\d+', line_stripped).group()
            current_chapter = f"chapter-{chapter_num.zfill(2)}"
            current_start = i
        elif re.match(r'^Foreword$', line_stripped, re.IGNORECASE):
            if current_chapter:
                boundaries.append((current_chapter, current_start, i))
            current_chapter = "foreword"
            current_start = i
        elif re.match(r'^Preface$', line_stripped, re.IGNORECASE):
            if current_chapter:
                boundaries.append((current_chapter, current_start, i))
            current_chapter = "preface"
            current_start = i
        elif re.match(r'^In\s+Closing$', line_stripped, re.IGNORECASE):
            if current_chapter:
                boundaries.append((current_chapter, current_start, i))
            current_chapter = "in-closing"
            current_start = i
    
    # Add last chapter
    if current_chapter:
        boundaries.append((current_chapter, current_start, len(lines)))
    
    return boundaries

def extract_chapter_content(lines, start, end, chapter_key):
    """Extract and clean chapter content"""
    content_lines = lines[start:end]
    content = '\n'.join(content_lines)
    
    # Remove chapter header lines
    content = re.sub(r'^CHAPTER\s+\d+.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^Foreword.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^Preface.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^In\s+Closing.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove chapter title line (next line after CHAPTER)
    if chapter_key.startswith("chapter-"):
        # Remove common title patterns
        content = re.sub(r'^(PHP Today|New Versions|PHP\'s Type System|Static Analysis|Property Promotion|Named Arguments|Attributes|Short Closures|Working with Arrays|Match|Object Oriented PHP|MVC Frameworks|Dependency Injection|Collections|Testing|Style Guide|The JIT|Preloading|FFI|Internals|Type Variance|Async PHP|Event Driven Development)\s*$', '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove "PART I", "PART II", etc. lines
    content = re.sub(r'^PART\s+[IVX]+.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^PHP, the Language.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^Building With PHP.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    content = re.sub(r'^PHP In Depth.*?\n', '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    return clean_text(content)

def get_chapter_title(chapter_key):
    """Get chapter title from key"""
    titles = {
        "foreword": "# FOREWORD",
        "preface": "# PREFACE",
        "in-closing": "# IN CLOSING",
        "chapter-01": "# CHAPTER 01\n\n## PHP TODAY",
        "chapter-02": "# CHAPTER 02\n\n## NEW VERSIONS",
        "chapter-03": "# CHAPTER 03\n\n## PHP'S TYPE SYSTEM",
        "chapter-04": "# CHAPTER 04\n\n## STATIC ANALYSIS",
        "chapter-05": "# CHAPTER 05\n\n## PROPERTY PROMOTION",
        "chapter-06": "# CHAPTER 06\n\n## NAMED ARGUMENTS",
        "chapter-07": "# CHAPTER 07\n\n## ATTRIBUTES",
        "chapter-08": "# CHAPTER 08\n\n## SHORT CLOSURES",
        "chapter-09": "# CHAPTER 09\n\n## WORKING WITH ARRAYS",
        "chapter-10": "# CHAPTER 10\n\n## MATCH",
        "chapter-11": "# CHAPTER 11\n\n## OBJECT ORIENTED PHP",
        "chapter-12": "# CHAPTER 12\n\n## MVC FRAMEWORKS",
        "chapter-13": "# CHAPTER 13\n\n## DEPENDENCY INJECTION",
        "chapter-14": "# CHAPTER 14\n\n## COLLECTIONS",
        "chapter-15": "# CHAPTER 15\n\n## TESTING",
        "chapter-16": "# CHAPTER 16\n\n## STYLE GUIDE",
        "chapter-17": "# CHAPTER 17\n\n## THE JIT",
        "chapter-18": "# CHAPTER 18\n\n## PRELOADING",
        "chapter-19": "# CHAPTER 19\n\n## FFI",
        "chapter-20": "# CHAPTER 20\n\n## INTERNALS",
        "chapter-21": "# CHAPTER 21\n\n## TYPE VARIANCE",
        "chapter-22": "# CHAPTER 22\n\n## ASYNC PHP",
        "chapter-23": "# CHAPTER 23\n\n## EVENT DRIVEN DEVELOPMENT",
    }
    return titles.get(chapter_key, f"# {chapter_key.upper()}")

def get_file_path(chapter_key):
    """Get file path for chapter"""
    if chapter_key == "foreword":
        return "foreword.md"
    elif chapter_key == "preface":
        return "preface.md"
    elif chapter_key == "in-closing":
        return "in-closing.md"
    elif chapter_key.startswith("chapter-"):
        num = chapter_key.split("-")[1]
        num_int = int(num)
        if num_int <= 10:
            return f"part-i-php-the-language/chapter-{num.zfill(2)}-{get_chapter_slug(num_int)}.md"
        elif num_int <= 16:
            return f"part-ii-building-with-php/chapter-{num.zfill(2)}-{get_chapter_slug(num_int)}.md"
        else:
            return f"part-iii-php-in-depth/chapter-{num.zfill(2)}-{get_chapter_slug(num_int)}.md"
    return None

def get_chapter_slug(num):
    """Get chapter slug from number"""
    slugs = {
        1: "php-today", 2: "new-versions", 3: "phps-type-system", 4: "static-analysis",
        5: "property-promotion", 6: "named-arguments", 7: "attributes", 8: "short-closures",
        9: "working-with-arrays", 10: "match", 11: "object-oriented-php", 12: "mvc-frameworks",
        13: "dependency-injection", 14: "collections", 15: "testing", 16: "style-guide",
        17: "the-jit", 18: "preloading", 19: "ffi", 20: "internals",
        21: "type-variance", 22: "async-php", 23: "event-driven-development"
    }
    return slugs.get(num, f"chapter-{num}")

def main():
    with open('pdf_text.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    boundaries = find_chapter_boundaries(lines)
    
    # Group boundaries by chapter key to merge content
    chapters = {}
    for chapter_key, start, end in boundaries:
        if chapter_key not in chapters:
            chapters[chapter_key] = []
        chapters[chapter_key].append((start, end))
    
    for chapter_key, ranges in chapters.items():
        # Merge all ranges for this chapter
        all_content = []
        for start, end in ranges:
            content = extract_chapter_content(lines, start, end, chapter_key)
            if content:
                all_content.append(content)
        
        if not all_content:
            continue
        
        # Combine all content
        combined_content = '\n\n'.join(all_content)
        
        file_path = get_file_path(chapter_key)
        
        if file_path:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
            
            # Write content
            title = get_chapter_title(chapter_key)
            full_content = f"{title}\n\n{combined_content}\n"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            total_lines = sum(end - start for start, end in ranges)
            print(f"Processed: {file_path} ({total_lines} lines, {len(ranges)} sections)")

if __name__ == "__main__":
    main()

