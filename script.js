const radio_btns = document.getElementsByClassName("radio_btn")

for (let i = 0; i < radio_btns.length; i++){
    radio_btns[i].addEventListener("change", function()
        {
            document.getElementsByClassName('hero')[0].style.display = "none";

        const containers = document.getElementsByClassName('tab_content_container');
        for (let i2 = 0; i2 < containers.length; i2++)
            { 
                containers[i2].style.display = "none";
                document.getElementById(containers[i].id).style.display = 'block';
            }
        }
    )
}