import React from 'react';
import "./Submenu.css";

export default function Shop_Submenu () {
    return (
        <div className="submenu">
            <div className="submenu-box">
                <ul className="submenu-list">
                    <p classname="title">Mua hàng</p>
                    <li><a href="#">Mua sản phẩm mới nhất</a></li>
                    <li><a href="#">Sạc</a></li>
                    <li><a href="#">Tai Nghe</a></li>
                    <li><a href="#">Phụ kiện</a></li>
                    <li><a href="#">Các mặt hàng khác</a></li>
                </ul>

                <ul className="submenu-list">
                    <p classname="title">Liên kết nhanh</p>
                    <li><a href="#">Tình trạng đơn hàng</a></li>
                    <li><a href="#">Hướng dẫn mua hàng</a></li>
                    <li><a href="#">Chính sách đổi trả</a></li>
                    <li><a href="#">Chính sách bảo hành</a></li>
                </ul>
            </div>
        </div>
    )
}