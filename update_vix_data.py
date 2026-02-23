import yfinance as yf
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def update_vix_data():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VIX 데이터 업데이트 시작")
    
    tickers = {
        '^VIX': 'VIX',      # CBOE Volatility Index
        'SPY':  'SPY',       # S&P 500 ETF
    }
    
    for yf_ticker, filename in tickers.items():
        try:
            print(f"  → {yf_ticker} 다운로드 중...")
            df = yf.download(yf_ticker, period='max', auto_adjust=False, progress=False)
            
            if df.empty:
                print(f"  ⚠ {yf_ticker}: 데이터 없음, 스킵")
                continue
            
            # MultiIndex 컬럼 처리
            if hasattr(df.columns, 'levels') and len(df.columns.levels) > 1:
                df.columns = df.columns.get_level_values(0)
            
            cols = ['Close', 'High', 'Low', 'Open', 'Volume']
            available_cols = [c for c in cols if c in df.columns]
            df = df[available_cols]
            
            filepath = os.path.join(DATA_DIR, f'{filename}.csv')
            df.to_csv(filepath)
            
            rows = len(df)
            last_date = df.index[-1].strftime('%Y-%m-%d')
            last_close = df['Close'].iloc[-1]
            print(f"  ✓ {filename}: {rows}행, 최종 {last_date}, {last_close:.2f}")
            
        except Exception as e:
            print(f"  ✗ {yf_ticker} 오류: {e}")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 업데이트 완료!")

if __name__ == '__main__':
    update_vix_data()
