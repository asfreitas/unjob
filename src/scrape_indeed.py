import scrapy, string

class IndeedSpider(scrapy.Spider):
    name='indeed_jobs'
    start_urls = ['https://www.indeed.com/q-Software-Engineer-l-Portland,-OR-jobs.html']

    def parse(self, response):       
        SCRAPE_INDEED = '.jobsearch-SerpJobCard'
        for jobListing in response.css(SCRAPE_INDEED):
            COMPANY_NAME = './/span[@class="company"]/a/text()'
            JOB_TITLE = './/a[@data-tn-element="jobTitle"]'
            JOB_TITLE3 = './/a[@data-tn-element="jobTitle"]/b/text()'
            JOB_TITLE2 = './/a[@data-tn-element="jobTitle"]/text()'
            outer_job_title = jobListing.xpath(JOB_TITLE).get()
            outer_job_title_bold = jobListing.xpath(JOB_TITLE3).getall()
            outer_job_title_reg = jobListing.xpath(JOB_TITLE2).get()
            concat_job_title = ''

            if outer_job_title_bold is not None:
                for bold in outer_job_title_bold:
                    concat_job_title = concat_job_title + bold + ' '
            concat_job_title = (concat_job_title + ' ' + outer_job_title_reg).strip()
            concat_job_title = ' '.join(concat_job_title.split())

            SUMMARY = './/span[@class="summary"]/text()'
            SUMMARY_BOLD = './/span[@class="summary"]/b/text()'
            summary2 = jobListing.xpath(SUMMARY).extract()
            summary_bold2 = jobListing.xpath(SUMMARY_BOLD).extract()

            concat_summary = ''
            concat_summary_bold = ''

            if summary_bold2 is not None:
                for bolds in summary_bold2:
                    concat_summary_bold = concat_summary_bold + bolds + ' '

            if summary2 is not None:
                for summy in summary2:
                    concat_summary.replace("\n","")
                    concat_summary = concat_summary + summy + ' '
                    if summy == ' ':
                        concat_summary = concat_summary + ' ' + concat_summary_bold + ' '

            concat_summary2 = ' '.join(concat_summary.split())
            #todo- this may repeat the job title a few times in a row in certain cases

            LOCATION = './/div[@data-rc-loc]'
            outer_location = jobListing.xpath(LOCATION).get()
            inner_loc = response.xpath(LOCATION).xpath("@data-rc-loc").extract()

            full_job_desc = jobListing.xpath("@data-jk").extract()
            full_job_desc_url = 'https://www.indeed.com/viewjob?jk=' + str(full_job_desc[0])

            #todo- get job apply link- call parse_job_app
            #if full_job_desc_url is not None:

            yield {
                'company': jobListing.xpath(COMPANY_NAME).get('').strip(),
                'title': concat_job_title,
                'location': inner_loc[0],
                'summary': concat_summary2,
                'summary_url': full_job_desc_url
            }

        ####all the code below works- uncomment when you want to scrape every page
        next_page_outer = './/link[@rel="next"]'
        next_page_url_outer = response.xpath(next_page_outer).get()
        next_page_url_href = response.xpath(next_page_outer).xpath("@href").extract()
        full_next_url = str('https://www.indeed.com') + next_page_url_href[0]
        
        if full_next_url is not None:
            yield scrapy.Request(full_next_url, callback=self.parse)

        #end of code that is used to scrape every page
        
    #todo- this is how you build job apply
    #you have to crawl the 
    #full description url page
    #you are looking for this:
    #<div id="jobsearch-ViewJobButtons-container
        #<div id="viewJobButtonLinkContainer"
            #<div class ... href="https://www.indeed.com/rc/clk?jk=77bea45fad51c8bd&amp;from=vj&amp;pos=bottom"
    #def parse_job_app(self, response):       
        #JOB_APP_PARSE = '.jobsearch-ViewJobButtons-container'
        #for jobPosting in response.css(JOB_APP_PARSE):
