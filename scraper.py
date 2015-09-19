from lxml import html
import requests
import re
import scraperwiki
import time

current_mp_ids = ["50","53","55","56","57","58","61","64","71","72","75","83","85","86","87","89","95","96","100","101","104","106","108","112","113","114","115","116","119","122","124","125","128","133","138","139","140","142","143","148","152","155","158","161","162","164","166","168","169","172","174","180","181","182","186","188","189","192","194","195","196","198","199","200","201","202","205","213","215","218","224","225","228","229","234","259","262","267","271","276","287","293","299","306","309","311","316","1242","1244","1247","1423","1431","1432","1444","1450","1459","1461","1467","1468","1469","1473","1476","1478","1482","1483","1499","1521","1579","1583","1590","2494","2868","2869","3014","3076","3127","3128","3132","3133","3136","3138","3139","3141","3142","3143","3144","3146","3147","3149","3151","3152","3153","3154","3155","3156","3160","3163","3164","3165","3166","3167","3168","3170","3171","3172","3176","3178","3179","3183","3185","3186","3188","3190","3191","3193","3194","3200","3201","3202","3203","3207","3208","3212","3213","3215","3216","3217","3219","3220","3221","3222","3223","3224","3225","3226","3227","3228","3230","3231","3232","3233","3234","3235","3236","3237","3238","3239","3240","3241","3242","3243","3244","3245","3246","3247","3248","3249","3250","3251","3252","3253","3254","3255","3257","3258","3259","3260","3261","3262","3263","3264","3265","3266","3268","3269","3270","3271","3272","3273","3274","3275","3276","3278","3279","3280"]
# These are current MP URL IDs as of 18 Sep 2015

def scrape_mps():
    for n in current_mp_ids:
        url = 'http://www.parliament.lk/en/members-of-parliament/directory-of-members/viewMember/' + str(n)
        page = requests.get(url)
        if page.status_code == 200:
            tree = html.fromstring(page.text)
            mp_name = tree.xpath('//div[@class="components-wrapper"]/h2/text()') 
            
            if mp_name:
                name = mp_name[0].split(',',1)[0]
                find_party = tree.xpath('//td[div="Party"]/a[1]/text()')
                if find_party:
                    party_list = find_party[0].split('(',1)
                    party = party_list[0]
                    party_id = party_list[1].split(')',1)[0]
                else:
                    party = ""  
                    party_id = ""                                  
                find_district = tree.xpath('//td[div="Electoral District / National List"]/text()') 
                if find_district:
                    area = find_district[0].strip()
                else:
                    area = ""
                find_email = tree.xpath('//a[@onclick="getContactUs();"]/text()') 
                if find_email:
                    email = find_email[0]
                else:
                    email = ""
                find_image = tree.xpath('//div[@class="left-pic"]/img/@src') 
                if find_image:
                    image = find_image[0]
                else:
                    image = ""
                find_birth_date = tree.xpath('//td[span="Date of Birth"]/text()') 
                if find_birth_date:
                    birth_date = find_birth_date[0].strip()
                    birth_date = re.search(r'\d{1,2}-\d{1,2}-\d{2,4}', birth_date).group()
                    birth_date = time.strptime(birth_date,'%d-%m-%Y')
                    try:
                        birth_date = time.strftime('%Y-%m-%d',birth_date)
                    except:
                        birth_date = ""
                else:
                    birth_date = ""
    
                data = {
                    'id': n,
                    'name': name,
                    'area': area,
                    'party': party,
                    'party_id': party_id,
                    'email': email,
                    'image': image,
                    'birth_date': birth_date,
                    'term': '15',
                    }
                
                scraperwiki.sqlite.save(unique_keys = ['id'], data = data)
                
            else:
                pass
        else:
            pass

          
scrape_mps()
