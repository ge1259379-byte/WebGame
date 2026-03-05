#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChatEn 英语语音生成器
使用gTTS快速生成英语语音MP3文件，避免重复生成
"""

import os
import json
import time
import sys
from pathlib import Path
from gtts import gTTS

# 设置控制台编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def generate_audio_gtts():
    """生成英语语音文件"""
    # 配置路径
    current_dir = Path(__file__).parent
    chat_script_dir = current_dir
    output_dir = current_dir.parent / "chatAudio"  # 在当前目录生成音频文件
    
    # 检查chatScript目录
    if not chat_script_dir.exists():
        print(f"[错误] chatScript目录不存在: {chat_script_dir}")
        return
    
    # 获取所有JSON文件
    json_files = list(chat_script_dir.glob("*.json"))
    if not json_files:
        print(f"[错误] 在 {chat_script_dir} 中未找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件")
    
    total_success = 0
    total_skipped = 0
    
    for json_file in json_files:
        print(f"\n处理: {json_file.name}")
        
        try:
            # 读取JSON文件
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 创建输出文件夹
            folder_name = json_file.stem
            folder_path = output_dir / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # 处理对话
            conversations = data.get('conversation', [])
            success_count = 0
            skipped_count = 0
            
            for index, conversation in enumerate(conversations):
                english_text = conversation.get('english', '')
                if not english_text:
                    continue
                
                # 生成文件名
                audio_filename = f"{folder_name}_{index}.mp3"
                audio_path = folder_path / audio_filename
                
                # 检查文件是否已存在
                if audio_path.exists():
                    print(f"  [跳过] {audio_filename}")
                    skipped_count += 1
                    continue
                
                try:
                    # 生成音频
                    tts = gTTS(text=english_text, lang='en', slow=False)
                    tts.save(str(audio_path))
                    print(f"  [成功] {audio_filename}")
                    success_count += 1
                    
                    # 短暂延迟避免请求过快
                    time.sleep(0.3)
                    
                except Exception as e:
                    print(f"  [失败] {audio_filename}: {e}")
            
            print(f"完成 {json_file.name}: 成功{success_count}, 跳过{skipped_count}")
            total_success += success_count
            total_skipped += skipped_count
            
        except Exception as e:
            print(f"[错误] 处理 {json_file.name} 失败: {e}")
    
    print(f"\n[完成] 总计: 成功{total_success}, 跳过{total_skipped}")

if __name__ == "__main__":
    print("=" * 50)
    print("WeChatEn 英语语音生成器")
    print("=" * 50)
    generate_audio_gtts()
    print("=" * 50)
