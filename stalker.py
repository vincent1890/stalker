from bs4 import BeautifulSoup
from requests import get
from os import system, makedirs
from re import search, findall


class GetInformation:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def twitter(user):
        twitter_media_url = f'https://twitter.com/{user}'

        try:
            html_page = get(twitter_media_url)
            soup = BeautifulSoup(html_page.text, 'html.parser')

            name = soup.find_all('a', class_='ProfileHeaderCard-nameLink u-textInheritColor js-nav')[0].get_text()

            count_media = soup.find_all('a', class_="PhotoRail-headingWithCount js-nav")[0].text
            count_media = search('\d+', count_media)
            count_media = count_media.group(0)

            bio = soup.find_all('p', class_="ProfileHeaderCard-bio u-dir")[0].text

            nav_values = soup.find_all('span', class_="ProfileNav-value")

            tweets_count = nav_values[0].text
            tweets_count = search('\d+', tweets_count)
            tweets_count = tweets_count.group(0)

            following_count = nav_values[1].text
            following_count = search('\d+', following_count)
            following_count = following_count.group(0)

            followers_count = nav_values[2].text
            followers_count = search('\d+', followers_count)
            followers_count = followers_count.group(0)

            information = {'user': user,
                           'name': name,
                           'tweetscount': tweets_count,
                           'followingcount': following_count,
                           'followerscount': followers_count,
                           'mediacount': count_media,
                           'bio': bio}

            return information
        except Exception as e:
            print('Erro:', e)


class DownloadMedia:

    def __init__(self, user):
        self.user = user

    @staticmethod
    def instagram(nick):
        try:
            path = f'./{nick}_[instagram]'
            makedirs(path)
        except FileExistsError:
            return 'This directory already exists, we will overwrite the existing files'
        try:
            arquivo = open('login-insta.txt', 'r')
            user_data = arquivo.readline()
            system(f'instagram-scraper {nick} {user_data} -d {path}')
            return 'Downloaded successfully!'
        except FileNotFoundError:
            system(f'instagram-scraper {nick}')
            return 'Downloaded successfully!'

    @staticmethod
    def facebook(user):
        print(f'Working on it\n{user} images will have to wait')

    @staticmethod
    def twitter(user):

        twitter_media_url = f'https://twitter.com/{user}/media'

        try:
            html_page = get(twitter_media_url)
            soup = BeautifulSoup(html_page.text, 'html.parser')

            images = soup.find_all('img')

            profile_picture_list = []
            image_banner_list = []
            image_banner = ''
            profile_picture = ''

            for item in images:
                profile_picture_item = search(r'https://pbs\.twimg\.com/profile_images/.+jpg', str(item))
                profile_picture_list.append(profile_picture_item)
                image_banner_item = search(r'https://pbs\.twimg\.com/profile_banners/.+1500x500', str(item))
                image_banner_list.append(image_banner_item)

            for item in profile_picture_list:
                if item:
                    profile_picture = item

            for item in image_banner_list:
                if item:
                    image_banner = item

            private_profile = soup.find('span', class_='ProfileHeaderCard-badges')

            print('')

            if private_profile:
                print('Private Profile is not supported')
            if not private_profile:
                path = f'./{user}_[twitter]'
                try:
                    makedirs(path)
                except FileExistsError:
                    pass

                try:
                    profile_picture_link = get(profile_picture.group())
                    with open(f"{path}\\Profile.jpg", "wb") as code:
                        code.write(profile_picture_link.content)
                    print('Profile picture downloaded')
                except AttributeError:
                    print('No Profile Pic')

                try:
                    image_banner_link = get(image_banner.group())
                    with open(f"{path}\\Banner.jpg", "wb") as code:
                        code.write(image_banner_link.content)
                    print('Banner downloaded')
                except AttributeError:
                    print('No Banner')

                try:
                    makedirs(f"{path}\\Media\\")
                except FileExistsError:
                    pass
                media_posts = soup.findAll('img', src=True)
                i = 0
                count = 0
                for _ in media_posts:
                    this_is_link = findall(r'https://pbs\.twimg\.com/media/.+.jpg', str(media_posts[i]))
                    if this_is_link:
                        for item in this_is_link:
                            count = count + 1
                            print(f'Downloading image #{count}')
                            media_post_link = get(item)
                            with open(f"{path}\\media\\{count}.jpg", "wb") as code:
                                code.write(media_post_link.content)
                    i += 1

            return 'Downloaded successfully!'
        except IndexError:
            return 'You must have entered the wrong username.'
