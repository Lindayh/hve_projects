// ---- Tabs ----

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

// ---- Form data validation ----
let val_array = [false, false, false, false]

// Empty fields check
const contact_form_fields = document.getElementsByClassName("form_input");
const email_field = document.getElementById("form_email");


for (let i = 0; i < contact_form_fields.length; i++)
{

    contact_form_fields[i].addEventListener("focusout", function()
    { 
        if (contact_form_fields[i].value == "")
            {
            contact_form_fields[i].style.border = "1px solid red";
            document.getElementsByClassName("form_alert")[i].textContent = "Empty field";

            val_array[i] = false; 
            }
        else
            {
            contact_form_fields[i].style.border = "none";       
            document.getElementsByClassName("form_alert")[i].textContent = "";
            
            val_array[i]= true;
            }


    }
    )

};

// Email specific validation
function email_validation ()
{
    if ( email_field.value !="" && ( (!(email_field.value.includes("@"))) || (!(email_field.value.includes("."))) || (email_field.value.includes(" ")) ) )
    {
        document.getElementsByClassName("form_alert")[1].textContent = "Invalid email";
        email_field.style.border = "1px solid red";

        val_array[1] = false;
    }
    else
    {
        document.getElementsByClassName("form_alert")[1].textContent = "";
        if (email_field.value == "")
        {
            document.getElementsByClassName("form_alert")[1].textContent = "Empty field";
        }
        val_array[1] = true;
    }
}

email_field.addEventListener("input", email_validation);
email_field.addEventListener("focusout", email_validation);



// Check on button click
const send_btn = document.getElementById("form_submit")
send_btn.addEventListener("click", function()
{
    if (val_array.includes(false))
    {
    alert("Invalid or missing data.");
    }
    else
    {
    document.getElementsByTagName("form")[0].removeAttribute("onsubmit")
    document.getElementsByTagName("form")[0].setAttribute("action","https://api.web3forms.com/submit")
    document.getElementsByTagName("form")[0].setAttribute("method","POST")

    alert("Mail was sent successfully.");
    }
}
)



// ---- Hide mobile menu ----

const tabs_content = document.getElementsByClassName("tab_content_container")

for (let i = 0; i < radio_btns.length; i++){
    radio_btns[i].addEventListener("change", function()
        {   
            if (window.matchMedia('(max-width: 600px)').matches)
            {
                document.getElementsByClassName("radio_container")[0].style.display = "none"
                document.getElementById("dl_cv_mobile").style.display = "none"
            }
        }
    )
}



