const url_api = "https://api.openweathermap.org/data/2.5/weather"

const key = "3b8f116a0e775bfe1369d9e18e75a6aa";

const url = `${url_api}?q=Stockholm&appid=${key}&units=metric&lang=sv`

https: fetch(url)
.then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('User Data:', data);
    console.log(`Stockholms temp: ${data.main.temp}; Description: ${data.weather[0].description}, Icon code: ${data.weather[0].icon}`)
    console.log(`Img url: https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`)

    let API_html_class = document.getElementsByClassName('weather_API')[0].children
    API_html_class[0].src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
    API_html_class[0].alt = `WIP`;

    API_html_class[1].getElementsByTagName('p')[1].textContent = `${data.main.temp} °C`

  })
  .catch(error => {
    console.error('Error:', error);
  });


