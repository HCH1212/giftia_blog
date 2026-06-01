.PHONY: git

git:
	git config user.email "hch20041214sr@qq.com"
	git config user.name "giftia"
	git add .
	git commit -m "update"
	git push


.PHONY: run

run:
	hugo server -D
