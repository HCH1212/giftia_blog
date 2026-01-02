.PHONY: git

git:
	git config --global user.email "hch20041214sr@qq.com"
	git config --global user.name "giftia"
	git add .
	git commit -m "update"
	git push
