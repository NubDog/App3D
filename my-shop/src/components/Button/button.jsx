import "./button.css"

export default function Button ({ children, variant = "main"}) {
    const variantClasses = {
        main: "main_button",
        sub: "sub_button",
        make_color: "make_color_button"
    }
    
    return <button className={variantClasses[variant]}>{children}</button>;
}