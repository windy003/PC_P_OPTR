import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def organize_screenshots(source_dir):
    """
    扫描指定目录下的PNG文件，按文件创建时间+3天分类到对应文件夹
    例如：文件创建于2025-11-08，会移动到2025-11-11文件夹

    Args:
        source_dir: 源目录路径
    """
    # 确保源目录存在
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"错误：目录 {source_dir} 不存在！")
        return

    # 统计信息
    processed_files = 0
    skipped_files = 0
    created_folders = set()

    # 遍历目录中的所有PNG文件
    for file_path in source_path.glob('*.png'):
        # 提取文件名
        filename = file_path.name

        # 获取文件的创建时间（时间戳）
        creation_time = os.path.getctime(str(file_path))

        # 将时间戳转换为datetime对象
        creation_date = datetime.fromtimestamp(creation_time)

        # 计算3天后的日期
        target_date = creation_date + timedelta(days=3)

        # 转换为日期字符串格式 YYYY-MM-DD
        date_str = target_date.strftime('%Y-%m-%d')

        print(f"文件: {filename}")
        print(f"  创建时间: {creation_date.strftime('%Y-%m-%d %H:%M:%S')} -> 目标文件夹: {date_str}")

        # 创建日期文件夹路径
        date_folder = source_path / date_str

        # 如果文件夹不存在，则创建
        if not date_folder.exists():
            date_folder.mkdir(parents=True, exist_ok=True)
            created_folders.add(date_str)
            print(f"  创建文件夹: {date_str}")

        # 移动文件到对应的日期文件夹
        dest_path = date_folder / filename

        # 如果目标文件已存在，跳过该文件
        if dest_path.exists():
            skipped_files += 1
            print(f"  跳过（文件已存在）: {filename}")
        else:
            # 移动文件
            shutil.move(str(file_path), str(dest_path))
            processed_files += 1
            print(f"  移动成功 -> {date_str}/")

        print()  # 空行，便于阅读

    # 输出统计信息
    print("\n" + "="*50)
    print(f"处理完成！")
    print(f"共创建 {len(created_folders)} 个文件夹")
    print(f"共移动 {processed_files} 个文件")
    print(f"跳过 {skipped_files} 个重复文件")
    print("="*50)

if __name__ == "__main__":
    # 自动识别用户家目录
    home_dir = Path.home()
    screenshots_dir = home_dir / "OneDrive" / "图片" / "Screenshots"

    print(f"开始整理截图文件...")
    print(f"源目录: {screenshots_dir}")
    print("="*50)

    organize_screenshots(str(screenshots_dir))
