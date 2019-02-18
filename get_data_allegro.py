
from lxml import html
from time import time
import requests
from tqdm import tqdm
positive_comments_file = "positive_comments.txt"
import time 

log_file = "downloading_log.txt"


positive_comments = []
with open(positive_comments_file,"a") as text_file:
    for i in (range(1)):
        try: 

            j = 1
            number_of_pages = 1
            while(j<=number_of_pages):
                page = requests.get("https://allegro.pl/uzytkownik/"+str(i)+"/oceny?recommend=true"+"&page="+str(j))
        
                tree = html.fromstring(page.content)
                    
                try:
                    number_of_pages = int(tree.xpath('//div[@class="ratings-pagination__list"]/span/text()')[1])

            
                except:
                    pass
            
                comments = tree.xpath('//span[@class="long-word-wrap"]/text()')
                positive_comments += comments
                text_file.write("\n".join(comments))
                    
                j+=1


        except:
            pass
    #print("finished downloading positive comments")
    #print("number of positive commments : " + str(len(positive_comments)))



      

    #print("saved positive comments to file: "+ positive_comments_file)

            



    negative_comments = []
    negative_comments_file ="negative_comments2.txt"

start_time =  time.time()

   

for i in (range(170000,1000000)):
    try:
        j = 1
        number_of_pages = 1
        while(j<=number_of_pages):
            page = requests.get("https://allegro.pl/uzytkownik/"+str(i)+"/oceny?recommend=false"+"&page="+str(j))
            
            tree = html.fromstring(page.content)
                
            try:
                number_of_pages = int(tree.xpath('//div[@class="ratings-pagination__list"]/span/text()')[1])

        
            except:
                pass
        
            comments = tree.xpath('//span[@class="long-word-wrap"]/text()')
            negative_comments += comments
            
            
            j+=1
            if((time.time()-start_time)>600):
                with open(negative_comments_file,"a") as text_file:
                    text_file.write("\n".join(negative_comments))
                    
                with open(log_file,"a") as file:
                    file.write(time.strftime('%d/%m/%Y ')+time.strftime("%H:%M:%S") + " Page number: " + str(i) + " Negative comments number: " + str(len(negative_comments))+"\n")
                
                start_time = time.time()
                negative_comments = []


    except:
        pass


#print("finished downloading negative comments")
#print("number of negative commments : " + str(len(negative_comments)))



    

#print("saved negative comments to file: "+ negative_comments_file)

