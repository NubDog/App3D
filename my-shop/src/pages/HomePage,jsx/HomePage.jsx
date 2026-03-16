import Header from "../../components/Header/header";
import Big_Banner from "../../components/Banner/big--banner";
import Big_banner_img_MacBook from "../../assets/img/hero_macbook_air_avail__fpm99qgohx2e_largetall.jpg";

const HomePage = () => {
    const main_link = "https://www.apple.com/vn/macbook-air/";
    const background_image = Big_banner_img_MacBook;
    const main_title_macbook_air = "MacBook Air";
    const sub_title_macbook_air = "Màu xanh da trời. \nHiệu năng cao ngất trời với M4.";
    const main_button_macbook_air = "Tìm hiểu thêm";
    const sub_button_macbook_air = "Mua";

    return (
        <div>
            <Header />
            <Big_Banner
                main_link={main_link}
                background_image={background_image}
                main_title={main_title_macbook_air}
                sub_title={sub_title_macbook_air}
                main_button={main_button_macbook_air}
                sub_button={sub_button_macbook_air}
            />
        </div>
    )
};

export default HomePage;