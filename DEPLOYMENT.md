- 通过git clone命令拉取当前项目的代码

  git clone https://github.com/cjy0826/mywork.git

- 利用Dockerfile文件构建镜像，使用docker build命令构建镜像并进行运行

  构建：docker build -t retrieval-tester .

  运行：docker run --rm -v ${PWD}/results:/mywork/results retrieval-tester

