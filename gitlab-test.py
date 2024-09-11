import base64
import gitlab
import os 

# 配置GitLab访问信息
GITLAB_URL = 'http://192.168.153.131'  # 替换为你的GitLab地址
#GITLAB_TOKEN = 'eECMKsgKQeiHF1668ys4'         # 替换为你的GitLab Personal Access Token
GITLAB_TOKEN = os.getenv("PUSH_TOKEN")         # 替换为你的GitLab Personal Access Token
FILE_PATH = 'argocd-devops-app/deployment.yaml'        # 替换为你要更新的文件路径
BRANCH_NAME = os.getenv("CI_COMMIT_BRANCH")                       # 替换为你要推送到的分支
#PROJECT_ID= 26
PROJECT_ID= os.getenv("CI_PROJECT_ID")

# 初始化GitLab对象
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

# 获取项目对象
project = gl.projects.get(PROJECT_ID)

# 获取当前文件内容
try:
    file = project.files.get(file_path=FILE_PATH, ref=BRANCH_NAME)
    print("当前文件内容:", file.decode())
except gitlab.exceptions.GitlabGetError:
    print(f"{FILE_PATH} 不存在，创建新文件...")

# 新的文件内容
with open(FILE_PATH, 'r') as file:
    new_content = file.read()
   


# 编码文件内容为base64
encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

# 提交文件到GitLab
data = {
    'branch': BRANCH_NAME,
    'commit_message': '更新文件内容  [ci skip]',
    'actions': [
        {
            'action': 'update',  # 如果文件不存在，可以用'create'来创建新文件
            'file_path': FILE_PATH,
            'content': new_content
        }
    ]
}

# 提交更改
try:
    commit = project.commits.create(data)
    print(f"文件已成功更新，提交ID: {commit.id}")
except Exception as e:
    print(f"提交失败: {e}")
