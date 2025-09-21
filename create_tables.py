#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import db

def main():
    print("MySQL 데이터베이스 테이블 생성 시작...")
    
    # 데이터베이스 연결
    if db.connect():
        print("✓ MySQL 데이터베이스 연결 성공")
        
        # 테이블 생성
        if db.create_tables():
            print("✓ 테이블 생성 완료")
            print("\n생성된 테이블:")
            print("- users: 사용자 정보")
            print("- submissions: 문제 제출 기록")
            print("- user_sessions: 사용자 세션 (향후 사용)")
        else:
            print("✗ 테이블 생성 실패")
    else:
        print("✗ MySQL 데이터베이스 연결 실패")
        print("\n확인사항:")
        print("1. MySQL 서버가 실행 중인지 확인")
        print("2. config.py의 데이터베이스 설정 확인")
        print("3. 데이터베이스 'coding_platform'이 생성되었는지 확인")
    
    # 연결 해제
    db.disconnect()

if __name__ == "__main__":
    main() 