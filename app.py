import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Tính Tiền Gửi Tiết Kiệm",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Công Cụ Tính Lãi Tiết Kiệm (Lãi Đơn & Lãi Kép)")
st.caption("Ứng dụng tính toán và so sánh lợi nhuận gửi tiết kiệm ngân hàng")

# Tạo 2 cột: Cột nhập dữ liệu và Cột hiển thị kết quả
col_input, col_result = st.columns([1, 2], gap="medium")

with col_input:
    st.subheader("📥 Thông tin khoản gửi")
    
    principal = st.number_input(
        "Số tiền gửi ban đầu (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )
    
    months = st.number_input(
        "Số tháng gửi:",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )
    
    annual_rate = st.number_input(
        "Lãi suất hàng năm (%/năm):",
        min_value=0.1,
        max_value=30.0,
        value=6.0,
        step=0.1
    )
    
    st.info(f"💡 **Tóm tắt:** Gửi **{principal:,.0f} đ** trong **{months} tháng** với lãi suất **{annual_rate}%/năm**.")

# Công thức tính toán
# 1. Lãi đơn: Tiền lãi = Gốc * (Lãi suất năm / 100) * (Số tháng / 12)
simple_interest = principal * (annual_rate / 100) * (months / 12)
total_simple = principal + simple_interest

# 2. Lãi kép (ghép lãi theo tháng): FV = P * (1 + r/12)^n
monthly_rate = (annual_rate / 100) / 12
total_compound = principal * ((1 + monthly_rate) ** months)
compound_interest = total_compound - principal

diff = compound_interest - simple_interest

with col_result:
    st.subheader("📊 Kết quả so sánh")
    
    # Hiển thị thẻ số liệu (Metrics)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="Tổng tiền (Lãi Đơn)",
            value=f"{total_simple:,.0f} đ",
            delta=f"+{simple_interest:,.0f} đ tiền lãi"
        )
    with m2:
        st.metric(
            label="Tổng tiền (Lãi Kép - Tháng)",
            value=f"{total_compound:,.0f} đ",
            delta=f"+{compound_interest:,.0f} đ tiền lãi"
        )
    with m3:
        st.metric(
            label="Chênh lệch lợi nhuận",
            value=f"{diff:,.0f} đ",
            delta="Lãi kép vượt trội",
            delta_color="normal"
        )
    
    st.divider()

    # Bảng chi tiết theo từng tháng để vẽ biểu đồ
    growth_data = []
    current_compound = principal
    
    for m in range(1, months + 1):
        # Lãi đơn tích lũy đến tháng m
        simp = principal + principal * (annual_rate / 100) * (m / 12)
        # Lãi kép tích lũy đến tháng m
        comp = principal * ((1 + monthly_rate) ** m)
        
        growth_data.append({
            "Tháng": m,
            "Lãi Đơn (VNĐ)": round(simp),
            "Lãi Kép (VNĐ)": round(comp)
        })
        
    df = pd.DataFrame(growth_data)
    
    # Biểu đồ trực quan hóa
    st.write("**Biểu đồ tăng trưởng số dư qua từng tháng:**")
    st.line_chart(df.set_index("Tháng"))

    # Bảng số liệu chi tiết (tùy chọn mở rộng)
    with st.expander("📄 Xem chi tiết số liệu từng tháng"):
        st.dataframe(
            df.style.format({
                "Lãi Đơn (VNĐ)": "{:,.0f}",
                "Lãi Kép (VNĐ)": "{:,.0f}"
            }),
            use_container_width=True
        )
