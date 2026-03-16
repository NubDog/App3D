import "./header.css";
import Shop_Submenu from "./Header_Submenu/Submenu";
import { useState } from "react";

const Header = () => {
    return (
        <div className="header">
            <ul className="header_list">
                <li className="header_item">
                    <a href="#"><i className="header_item-attribute fa-brands fa-xbox"></i></a>
                </li>

                <li className="header_item submenu-container">
                    <a href="#" className="header_item-attribute">
                        Cửa hàng
                    </a>
                    <Shop_Submenu />
                </li>

                <li className="header_item">
                    <a href="#" className="header_item-attribute">Tai Nghe</a>
                </li>

                <li className="header_item">
                    <a href="#" className="header_item-attribute">Sạc</a>
                </li>

                <li className="header_item">
                    <a href="#" className="header_item-attribute">Văn Vở</a>
                </li>

                <li className="header_item">
                    <a href="#" className="header_item-attribute">Đăng nhập</a>
                </li>

                <li className="header_item">
                    <i className="header_item-attribute fa-solid fa-magnifying-glass"></i>
                </li>

                <li className="header_item">
                    <a href="#"><i className="header_item-attribute fa-solid fa-bag-shopping"></i></a>
                </li>
            </ul>
        </div>
    )
}

export default Header;