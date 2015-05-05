##fly_offer
    a website for helping real programmer get better offer
    ![preview1](https://raw.githubusercontent.com/AssassinPig/flying_offer/master/images/preview1.png)
    ![preview2](https://raw.githubusercontent.com/AssassinPig/flying_offer/master/images/preview2.png)

1. archive
    1. a simple search engine
        1. crawler_task
            spider 爬取数据所用
        2. parser
            解析爬去下的网页 并保存
        3. index_builder
            建立索引
        4. query_man
            searcher  提供查询服务
    2. website
        it is written by flask using python

2. usage:
    1. preparation 
        1. prepare directionary
            ```
                mkdir data
                mkdir cleaned_data
            ```
        2. start redis

    2. crawl data 
        ```
            python crawler_task
        ```
        or you can write custom spider
        br
        a better distribution crawler for your reference which is also written by me-- [viper-py](https://github.com/AssassinPig/viper-py.git)
        the page data will put in directionary data you mkdir just now 

    3. parse data and build index
        ```
            python index_build.py
        ```
        the cleaned data will exculded all html tags and then will be put in directionary cleaned_data
        br
        It is a better way to parse page for extracting clean data and build index in the same step 

    4. query service
        this step programme is query_man.py

    5. run website
        ```
            python app.py
        ```
3. todo
    1. model.py optimizing
    2. query suggestion function
    3. query result display optimizting
