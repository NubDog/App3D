import "./big--banner.css";
import Button from "../Button/button.jsx";

const Big_Banner = ({main_link,
    background_image,
    main_title,
    sub_title,
    main_button,
    sub_button,

}) => {
    return (
        <div className="big--banner" style={{backgroundImage: `url(${background_image})`}}>
            <a className="big--banner_link" href={main_link}></a>

            <div className="big--banner_content">
                <div className="big--banner_content_title">
                    <h3>{main_title}</h3>
                    <p>{sub_title}</p>
                </div>

                <div className="big--banner_button">
                    {/* 2 cái button cũ nằm ở đây */}
                    {/* <Button variant="main">{main_button}</Button>
                    <Button variant="sub">{sub_button}</Button> */}

                    {/* còn đây là 2 cái button mới */}
                    <a variant="make_color_button" href={main_link}>{main_button}</a>
                    <a variant="make_color_button" href={sub_link}>{sub_button}</a>
                </div>
            </div>
        </div>
    )
}

export default Big_Banner;