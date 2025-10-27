# mywork

项目地址：[cjy0826/mywork: 大作业](https://github.com/cjy0826/mywork)

* 1、APP：开发机器学习相关的代码，模拟CIFAR-10训练，便于测试，对一些复杂的训练逻辑进行删减；完成本地测试。

  相关代码及文件：
  ***app/retrieval.py	训练代码***
  ***app/test_retrieval.py	测试python程序代码***

* 2、Version Control：在github上创建仓库、分支，实现项目代码的版本控制，项目地址：

  https://github.com/cjy0826/mywork.git

* 3、Docker：编写Dockerfile文件，将python程序容器化；

  相关代码及文件：

  ***Dockerfile	用于构建docker镜像***

  ***requirements.txt	python程序依赖包清单文件，用于构建镜像时下载相关依赖包***

  ***.dockerignore	避免其他不相关文件构建到镜像中***

  完成本地容器化部署后，运行镜像容器，测试程序是否可运行得到目标输出结果

* 4、CI/CD：在github上配置自动化测试和持续集成工作流，进行代码检查、格式化检查

  相关代码及文件：

  ***.github/workflows/ci.yml	用于自动化测试和持续集成的工作流程配置***

  ① Commit，开发提交，本地完成开发后提交到远程仓库，触发代码静态检查

  ② Build，构建阶段，验证代码能否成功构建并推送到镜像仓库

  ③ Test，测试阶段，在CI环境运行完整的测试，自动进行

  ④ Staging，预发布环境，在预发布服务器部署构建镜像进行验证

  ⑤ Production，生产环境，也就是正式运行环境，构建正式的Docker镜像并部署到生产

  在ci.yml配置中，对staging、dev、main这三个分支都会触发事先定义的工作流程

* 5、DVC：数据版本控制，初始化dvc，对数据文件生成对应的data.dvc文件，并将dvc相关文件上传到github，将数据文件通过dvc上传到云存储器，如阿里云oss。

  相关代码及文件：

  ***.dvc	dvc初始化文件***

  ***.dvcignore	dvc初始化文件，排除不需要上传的数据***

  ***data.dvc	使用dvc命令提交数据文件data目录后形成相应的dvc数据跟踪文件，该文件上传到github用于数据跟踪***
  将敏感参数如（secret）进行参数化配置，如dvc中的远程oss的敏感信息id、secret进行参数化配置：

  ```
  [core]
      remote = myoss
  ['remote "myoss"']
      url = oss://bucket-cjy/dvc
      oss_endpoint = oss-cn-wuhan-lr.aliyuncs.com
      oss_key_id = ${ALIBABA_ACCESS_KEY_ID}
      oss_key_secret = ${ALIBABA_ACCESS_KEY_SECRET}
  ```

​	在环境变量中对变量进行赋值，如export ALIBABA_ACCESS_KEY_ID=xxxxxxx等。在github中进行Action工作流程的secret设置，包括Environment secrets与Environment variable。