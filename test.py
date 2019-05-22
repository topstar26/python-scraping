from bs4 import BeautifulSoup
import requests
import csv
i = 1
#CSV File Read and Input the Headline
csv_file = open('site_blog.csv', 'w', encoding='UTF-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Main Address', 'Type', 'Website Address', 'Telephone Number', 'Specialist', 'Partner Status', 'Experience', 'Certification', 'Certification', 'Certification', 'Facebook', 'Twitter', 'Linkedin', 'Name', 'Position','Industries Served', 'Connected Apps', 
'Office Address Number 1', 'Office Address Telephone number 1', 
'Office Address Number 2', 'Office Address Telephone number 2', 'Office Address Number 3', 
'Office Address Telephone number 3', 'Office Address Number 4', 'Office Address Telephone number 4',  'Office Address Number 5', 'Office Address Telephone number 5',
'Office Address Number 6', 'Office Address Telephone number 6', 'Office Address Number 7', 'Office Address Telephone number 7', 'Office Address Number 8', 'Office Address Telephone number 8',
    'Office Address Number 9', 'Office Address Telephone number 9', 'Office Address Number 10', 'Office Address Telephone number 10' ])   

for i in range(255): 
    source = requests.get('https://www.xero.com/uk/advisors/find-advisors/?type=advisors&orderBy=ADVISOR_RELEVANCE&sort=ASC&location=47.5554486,-18.531958900000063,61.5471111,9.584415700000022&pageNumber=' + str(i+1) + '&place-name=United%20Kingdom&country=GB&view=list').text
    soup = BeautifulSoup(source, 'lxml')
    target_url= []
    
    print('current page:'+str(i+1))

    for post in soup.findAll('div', {'class':'advisors-result-card'}):
        target_url.append(post.a['href'])
        # print(post.a['href'])

  
    for url in target_url:
        # print(url)   
        main_page = requests.get(url)
        html = main_page.text
        main = BeautifulSoup(html, 'lxml')

        ## ----------------Employer Information-------------------- ##
        employers = main.find_all('article')

        if len(employers) > 0:

            for employer in employers:     
                employer_pos = employer.find('p',class_='advisors-profile-team-role')
                employer_name_str = employer.h3.text.strip()

                try:
                    employer_position_str = employer_pos.text.strip()
                except Exception as e:
                    employer_position_str = ''

                ## ------------------- Website Info --------------------- ##
                try:
                    website_name = main.find('h1', class_='title-2').text
                # print(website_name)

                except Exception as e:
                    website_name = ''
                try:
                    description = main.find('p', class_='advisors-profile-hero-detailed-info-sub').text
                    description = description.split('·')
                    website_type = description[0].strip()
                except Exception as e:
                    description = ''
                    website_type = ''
                # print(website_type)

                if len(description) > 1:
                    main_address = description[1].strip()
                    print(main_address)
                    try:

                        website_address= main.find('a', class_='advisors-profile-hero-detailed-contact-website')['href']
                        # print(website_address)

                        telephone_number = main.find('a', class_='advisors-profile-hero-detailed-contact-phone')['data-phone']
                        # print(telephone_number)
                    except Exception as e:
                        website_address = ''
                        telephone_number = ''
                else:
                    website_address = ''
                    telephone_number = ''
                ## --------- Profile Badges -------------##
                main_badges = main.find('div', class_='TagGroup__TagSection-s1xhwdnt-1')
                profile_badges = main_badges.find_all('div', class_='exqQEg')
                # profile_badges_titles = main.find_all('p', class_='gWwNyz')

                

                specialist = ''
                partner_status = ''
                experience = ''
                certifications = []
                # for profile_badges_title in profile_badges_titles:
                #     print(profile_badges_title.text)
                for profile_badge in profile_badges:
                    badge_title = profile_badge.find('p', class_='gWwNyz').text.strip()
                    badge_content = profile_badge.find('h6', class_='Tag__TagHeading-tkc026-2').text.strip()
                    if badge_title == 'Specialist':
                        specialist = badge_content
                    elif badge_title == 'Partner status':
                        partner_status = badge_content
                    elif badge_title == 'Experience':
                        experience = badge_content
                    elif badge_title == 'Certification':
                        certifications.append(badge_content)
                # print('Specialist:' + specialist)
                # print('Partner Status:'+ partner_status)
                # print('Experience:'+ experience)
                i = 0
                
                certification1 = ''
                certification2 = ''
                certification3 = ''
                while i < len(certifications):
                    
                    try:
                        if i == 0:
                            certification1 = certifications[i]
                        elif i == 1:
                            certification2 = certifications[i]
                        elif i == 2:
                            certification3 = certifications[i]
                        i += 1
                    except Exception as e:
                        break          
                # certification_str = '\r\n'.join(certifications)
                # print('Certification:' + certification_str)
            

                ##----------- Social link ------------## 
                social = main.find_all('a', class_='advisor-profile-practice-social-link') 
                facebook = ''
                twitter = ''
                linkedin = ''
                for social_link in social:
                    social_name = social_link.text.strip()
                    try:
                        social_url = social_link['href'].strip()
                    except Exception as e:
                        social_url = ''
                    if social_name == 'Facebook':
                        facebook = social_url
            
                    elif social_name == 'Twitter':
                        twitter = social_url
                
                    elif social_name == 'LinkedIn':
                        linkedin = social_url     

                # print('Facebook: ' + facebook)
                # print('Twitter: ' + twitter)
                # print('LinkedIn: ' + linkedin)



            ## --------------- Bank Connection & Industires Seved ----------------- ##
                bank_industries = main.find_all('ul', class_='kjlzfe')
                
            ## --------------- Bank Connections ------------------------ ##
                # bank_connections = bank_industries[0]
                # bank_connection = []
                # for bank in bank_connections:
                #     bank_connection.append(bank.text.strip())
                #     print(bank.text)
                
            ## ---------------- Industries Served ---------------------- ##
                is_industry = main.find_all('h4', class_='frIZwA')
                if len(is_industry) > 1:
                    try:
                        industries = bank_industries[1]
                    except Exception as e:
                        industries = ''
                    industry_serve = []
                    for industry in industries:
                        industry_serve.append(industry.text.strip())
                        # print(industry.text)
                    industry_serve_str = ', \r\n'.join(industry_serve)
                elif len(is_industry) == 1:
                    if is_industry[0].text.strip() == 'Industries Served':
                        try:
                            industries = bank_industries[0]
                        except Exception as e:
                            industries = ''
                        industry_serve = []
                        for industry in industries:
                            industry_serve.append(industry.text.strip())
                            print(industry.text)
                        industry_serve_str = ', \r\n'.join(industry_serve)
                    else:
                        industry_serve_str = ''
                else:
                    industry_serve_str = ''

            ## ------------------ Connected Apps --------------------- ##
                connected_apps = main.find_all('a', class_='advisors-profile-experience-app')
                apps = []
                for connected_app in connected_apps:
                    app_name = connected_app.find('img', class_='advisors-profile-experience-app-icon')['alt']
                    apps.append(app_name)
                    # print(app_name)
                apps_str = ', \r\n'.join(apps)

            ## ------------------ Office Info ------------------------- ##
                contacts = main.find_all('dl', class_='advisors-profile-locations-list-item')
                contact_addresses = []
                contact_phones = []
                for contact in contacts:
                    
                    contact_address = contact.find('dd', class_='advisors-profile-locations-list-item-address').text.strip()
                    # contact_address = contact_address.p.text
                    contact_phone = contact.find('dd', class_='advisors-profile-locations-list-item-phone').text.strip()
                    # contact_phone = contact_phone.p.a.text
                    contact_addresses.append(contact_address)
                    contact_phones.append(contact_phone)
                    # contact_info = 'contact_name:' + contact_name + u'\u2386'+'contact_address:' + contact_address + '\015contact_phone:' + contact_phone
                    # print(f'contact_address:{contact_address}   contact_phone:{contact_phone}') 
                
                i = 0
                office_address1 = ''
                office_phone1 = ''
                office_address2 = ''
                office_phone2 = ''
                office_address3 = ''
                office_phone3 = ''
                office_address4 = ''
                office_phone4 = ''
                office_address5 = ''
                office_phone5 = ''
                office_address6 = ''
                office_phone6 = ''
                office_address7 = ''
                office_phone7 = ''
                office_address8 = ''
                office_phone8 = ''
                office_address9 = ''
                office_phone9 = ''
                office_address10 = ''
                office_phone10 = ''
                office_address11 = ''
                office_phone11 = ''
            
                while i < len(contact_addresses):
                    
                    try:
                        if i == 0:
                            office_address1 = contact_addresses[i]
                            office_phone1 = contact_phones[i]
                        elif i == 1:
                            office_address2 = contact_addresses[i]
                            office_phone2 = contact_phones[i]
                        elif i == 2:
                            office_address2 = contact_addresses[i]
                            office_phone2 = contact_phones[i]
                        elif i == 3:
                            office_address3 = contact_addresses[i]
                            office_phone3 = contact_phones[i]
                        elif i == 4:
                            office_address4 = contact_addresses[i]
                            office_phone4 = contact_phones[i]
                        elif i == 5:
                            office_address5 = contact_addresses[i]
                            office_phone5 = contact_phones[i]
                        elif i == 6:
                            office_address6 = contact_addresses[i]
                            office_phone6 = contact_phones[i]
                        elif i == 7:
                            office_address7 = contact_addresses[i]
                            office_phone7 = contact_phones[i]
                        elif i == 8:
                            office_address8 = contact_addresses[i]
                            office_phone8 = contact_phones[i]
                        elif i == 9:
                            office_address9 = contact_addresses[i]
                            office_phone9 = contact_phones[i]
                        elif i == 10:
                            office_address10 = contact_addresses[i]
                            office_phone10 = contact_phones[i]
                        i += 1
                    except Exception as e:
                        break   
                csv_writer.writerow([website_name, main_address, website_type, website_address, telephone_number, specialist, partner_status, experience, certification1 , certification2 , certification3, facebook, twitter, linkedin, employer_name_str, employer_position_str, industry_serve_str, apps_str
                , office_address1, office_phone1, office_address2, office_phone2, office_address3, office_phone3, office_address4, office_phone4, office_address5, office_phone5,
                office_address6, office_phone6, office_address7, office_phone7, office_address8, office_phone8, office_address9, office_phone9, office_address10, office_phone10, ])
        else:
            employer_name_str = ''
            employer_position_str = ''

            ## ------------------- Website Info --------------------- ##
            try:
                website_name = main.find('h1', class_='title-2').text
            # print(website_name)

            except Exception as e:
                website_name = ''
            try:
                description = main.find('p', class_='advisors-profile-hero-detailed-info-sub').text
                description = description.split('·')
                website_type = description[0].strip()
            except Exception as e:
                description = ''
                website_type = ''
            # print(website_type)

            if len(description) > 1:
                main_address = description[1].strip()
                print(main_address)
                try:

                    website_address= main.find('a', class_='advisors-profile-hero-detailed-contact-website')['href']
                    # print(website_address)

                    telephone_number = main.find('a', class_='advisors-profile-hero-detailed-contact-phone')['data-phone']
                    # print(telephone_number)
                except Exception as e:
                    website_address = ''
                    telephone_number = ''
            else:
                website_address = ''
                telephone_number = ''
            ## --------- Profile Badges -------------##
            main_badges = main.find('div', class_='TagGroup__TagSection-s1xhwdnt-1')
            profile_badges = main_badges.find_all('div', class_='exqQEg')

            

            specialist = ''
            partner_status = ''
            experience = ''
            certifications = []
            # for profile_badges_title in profile_badges_titles:
            #     print(profile_badges_title.text)
            for profile_badge in profile_badges:
            
                badge_title = profile_badge.find('p', class_='gWwNyz').text.strip()
                badge_content = profile_badge.find('h6', class_='glXkQW').text.strip()
                
                if badge_title == 'Specialist':
                    specialist = badge_content
                elif badge_title == 'Partner status':
                    partner_status = badge_content
                elif badge_title == 'Experience':
                    experience = badge_content
                elif badge_title == 'Certification':
                    certifications.append(badge_content)
            # print('Specialist:' + specialist)
            # print('Partner Status:'+ partner_status)
            # print('Experience:'+ experience)
            i = 0
            
            certification1 = ''
            certification2 = ''
            certification3 = ''
            while i < len(certifications):
                
                try:
                    if i == 0:
                        certification1 = certifications[i]
                    elif i == 1:
                        certification2 = certifications[i]
                    elif i == 2:
                        certification3 = certifications[i]
                    i += 1
                except Exception as e:
                    break          
            # certification_str = '\r\n'.join(certifications)
            # print('Certification:' + certification_str)
        

            ##----------- Social link ------------## 
            social = main.find_all('a', class_='advisor-profile-practice-social-link') 
            facebook = ''
            twitter = ''
            linkedin = ''
            for social_link in social:
                social_name = social_link.text.strip()
                social_url = social_link['href'].strip()
                
                if social_name == 'Facebook':
                    facebook = social_url
        
                elif social_name == 'Twitter':
                    twitter = social_url
            
                elif social_name == 'LinkedIn':
                    linkedin = social_url     

            # print('Facebook: ' + facebook)
            # print('Twitter: ' + twitter)
            # print('LinkedIn: ' + linkedin)



        ## --------------- Bank Connection & Industires Seved ----------------- ##
            bank_industries = main.find_all('ul', class_='kjlzfe')
            
        ## --------------- Bank Connections ------------------------ ##
            # bank_connections = bank_industries[0]
            # bank_connection = []
            # for bank in bank_connections:
            #     bank_connection.append(bank.text.strip())
            #     print(bank.text)
            
        ## ---------------- Industries Served ---------------------- ##
            is_industry = main.find_all('h4', class_='frIZwA')
            if len(is_industry) > 1:
                try:
                    industries = bank_industries[1]
                except Exception as e:
                    industries = ''
                industry_serve = []
                for industry in industries:
                    industry_serve.append(industry.text.strip())
                    # print(industry.text)
                industry_serve_str = ', \r\n'.join(industry_serve)
            elif len(is_industry) == 1:
                if is_industry[0].text.strip() == 'Industries Served':
                    try:
                        industries = bank_industries[0]
                    except Exception as e:
                        industries = ''
                    industry_serve = []
                    for industry in industries:
                        industry_serve.append(industry.text.strip())
                        print(industry.text)
                    industry_serve_str = ', \r\n'.join(industry_serve)
                else:
                    industry_serve_str = ''
            else:
                industry_serve_str = ''

        ## ------------------ Connected Apps --------------------- ##
            connected_apps = main.find_all('a', class_='advisors-profile-experience-app')
            apps = []
            for connected_app in connected_apps:
                app_name = connected_app.find('img', class_='advisors-profile-experience-app-icon')['alt']
                apps.append(app_name)
                # print(app_name)
            apps_str = ', \r\n'.join(apps)

        ## ------------------ Office Info ------------------------- ##
            contacts = main.find_all('dl', class_='advisors-profile-locations-list-item')
            contact_addresses = []
            contact_phones = []
            for contact in contacts:
                
                contact_address = contact.find('dd', class_='advisors-profile-locations-list-item-address').text.strip()
                # contact_address = contact_address.p.text
                contact_phone = contact.find('dd', class_='advisors-profile-locations-list-item-phone').text.strip()
                # contact_phone = contact_phone.p.a.text
                contact_addresses.append(contact_address)
                contact_phones.append(contact_phone)
                # contact_info = 'contact_name:' + contact_name + u'\u2386'+'contact_address:' + contact_address + '\015contact_phone:' + contact_phone
                # print(f'contact_address:{contact_address}   contact_phone:{contact_phone}') 
            
            i = 0
            office_address1 = ''
            office_phone1 = ''
            office_address2 = ''
            office_phone2 = ''
            office_address3 = ''
            office_phone3 = ''
            office_address4 = ''
            office_phone4 = ''
            office_address5 = ''
            office_phone5 = ''
            office_address6 = ''
            office_phone6 = ''
            office_address7 = ''
            office_phone7 = ''
            office_address8 = ''
            office_phone8 = ''
            office_address9 = ''
            office_phone9 = ''
            office_address10 = ''
            office_phone10 = ''
            office_address11 = ''
            office_phone11 = ''
        
            while i < len(contact_addresses):
                
                try:
                    if i == 0:
                        office_address1 = contact_addresses[i]
                        office_phone1 = contact_phones[i]
                    elif i == 1:
                        office_address2 = contact_addresses[i]
                        office_phone2 = contact_phones[i]
                    elif i == 2:
                        office_address2 = contact_addresses[i]
                        office_phone2 = contact_phones[i]
                    elif i == 3:
                        office_address3 = contact_addresses[i]
                        office_phone3 = contact_phones[i]
                    elif i == 4:
                        office_address4 = contact_addresses[i]
                        office_phone4 = contact_phones[i]
                    elif i == 5:
                        office_address5 = contact_addresses[i]
                        office_phone5 = contact_phones[i]
                    elif i == 6:
                        office_address6 = contact_addresses[i]
                        office_phone6 = contact_phones[i]
                    elif i == 7:
                        office_address7 = contact_addresses[i]
                        office_phone7 = contact_phones[i]
                    elif i == 8:
                        office_address8 = contact_addresses[i]
                        office_phone8 = contact_phones[i]
                    elif i == 9:
                        office_address9 = contact_addresses[i]
                        office_phone9 = contact_phones[i]
                    elif i == 10:
                        office_address10 = contact_addresses[i]
                        office_phone10 = contact_phones[i]
                    i += 1
                except Exception as e:
                    break   
            csv_writer.writerow([website_name, main_address, website_type, website_address, telephone_number, specialist, partner_status, experience, certification1 , certification2 , certification3, facebook, twitter, linkedin, employer_name_str, employer_position_str, industry_serve_str, apps_str
            , office_address1, office_phone1, office_address2, office_phone2, office_address3, office_phone3, office_address4, office_phone4, office_address5, office_phone5,
            office_address6, office_phone6, office_address7, office_phone7, office_address8, office_phone8, office_address9, office_phone9, office_address10, office_phone10, ])
csv_file.close() 