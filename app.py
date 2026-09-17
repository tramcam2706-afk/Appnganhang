import streamlit as st
st.image("logo.jpg")
from datetime import date, timedelta
from calendar import monthrange
 
# =========================================================
# CẤU HÌNH
# =========================================================
st.set_page_config(
   page_title="Tính lãi tiền gửi tiết kiệm",
   page_icon="💰",
   layout="wide"
)
 
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính theo ngày gửi → trước ngày đến hạn/rút tiền 1 ngày. Rút trước hạn áp dụng lãi suất không kỳ hạn.")
 
# =========================================================
# HÀM HỖ TRỢ
# =========================================================
def add_months(d, months):
   """Cộng số tháng, giữ ngày nếu có thể; nếu không lấy ngày cuối tháng."""
   total = d.year * 12 + (d.month - 1) + months
   year = total // 12
   month = total % 12 + 1
   day = min(d.day, monthrange(year, month)[1])
   return date(year, month, day)
 
