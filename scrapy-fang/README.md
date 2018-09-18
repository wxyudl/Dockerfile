## 大连每日房价脚本

#### STEPS:
```
1. Clone project from github
cd /scrapy/fang
git clone https://github.com/wxyudl/playdata.git

2. Set git ssh
cd /scrapy/fang/playdata
git branch
git checkout data
ssh-keygen -t rsa -C "wangxiaoyu_205@163.com"
cat ~/.ssh/id_rsa.pub

3. Copy ssh key and paste to github ssh setting

4. Test
ssh -T git@github.com

5. Config git remote url
vim .git/config
git@github.com:wxyudl/playdata.git
```