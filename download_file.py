#!/usr/bin/env python3
"""
URL에서 파일을 다운로드하여 임시 폴더에 저장하는 스크립트
"""

import os
import urllib.error
import urllib.request
from urllib.parse import urlparse


def download_file_to_temp(url, temp_dir="./temp"):
    """
    지정된 URL에서 파일을 다운로드하여 임시 폴더에 저장합니다.

    Args:
        url (str): 다운로드할 파일의 URL
        temp_dir (str): 임시 폴더 경로 (기본값: "./temp")

    Returns:
        str: 다운로드된 파일의 전체 경로
    """
    try:
        # 임시 폴더가 존재하지 않으면 생성
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print(f"임시 폴더를 생성했습니다: {temp_dir}")

        # URL에서 파일명 추출
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # 파일명이 없거나 '/'로 끝나는 경우 기본 파일명 사용
        if not filename or filename == "/":
            filename = "downloaded_file"

        # 전체 파일 경로 생성
        file_path = os.path.join(temp_dir, filename)

        print(f"다운로드 시작: {url}")
        print(f"저장 위치: {file_path}")

        # 파일 다운로드
        urllib.request.urlretrieve(url, file_path)

        # 파일 크기 확인
        file_size = os.path.getsize(file_path)
        print(f"다운로드 완료! 파일 크기: {file_size:,}", "bytes")

        return file_path

    except urllib.error.URLError as e:
        print(f"URL 오류: {e}")
        raise
    except OSError as e:
        print(f"파일 시스템 오류: {e}")
        raise
    except Exception as e:
        print(f"알 수 없는 오류: {e}")
        raise


def main():
    """메인 실행 함수"""
    url = "https://spri.kr/download/23735"

    try:
        downloaded_path = download_file_to_temp(url)
        print(f"\n성공! 파일이 다음 위치에 저장되었습니다:\n{downloaded_path}")

        # 다운로드된 파일 목록 확인
        temp_dir = "./temp"
        if os.path.exists(temp_dir):
            files = os.listdir(temp_dir)
            print("\n임시 폴더의 파일 목록:")
            for file in files:
                file_path = os.path.join(temp_dir, file)
                size = os.path.getsize(file_path)
                print(f"  {file} ({size:,} bytes)")

    except Exception as e:
        print(f"다운로드 실패: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
