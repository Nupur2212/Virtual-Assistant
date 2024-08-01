from requests_html import HTMLSession
import speech_to_text

def weather():
    s=HTMLSession()
    query="patna"
    url=f"https://www.google.com/search?q=weather+{query}"
    r=s.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    # temp=r.html.find('span#wob_tm',first=True).text
    # print(temp)
    # unit=r.html.find('div.vk_bk wob-unit span.wob_t',first=True).text
    # print(unit)
    # desc=r.html.find('span#wob_dc',first=True).text
    # print(desc)
    # return temp+" "+unit+" "+desc
    try:
        temp_element = r.html.find('span#wob_tm', first=True)
        unit_element = r.html.find('div.vk_bk span.wob_t', first=True)
        desc_element = r.html.find('span#wob_dc', first=True)

        if temp_element and unit_element and desc_element:
            temp = temp_element.text
            unit = unit_element.text
            desc = desc_element.text
            print(temp, unit, desc)
            return f"{temp} {unit}, {desc}"
        else:
            return "Weather information not found."

    except Exception as e:
        print("An error occurred:", e)
        return "Failed to retrieve weather information."