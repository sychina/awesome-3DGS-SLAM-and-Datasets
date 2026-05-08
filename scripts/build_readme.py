import yaml

# 1. 读取 papers.yml
with open("../data/papers.yml", "r") as f:
    papers = yaml.safe_load(f)

# 2. 排序，比如按年份降序
papers.sort(key=lambda x: x["year"], reverse=True)

# 3. 生成 markdown 表格
table = "| Year | Title | Authors | Modality | Tags | Paper | Code | Project | Local Eval |\n"
table += "|------|-------|---------|---------|------|-------|------|--------|-----------|\n"
for p in papers:
    title_link = f"[{p['title']}]({p['paper']})" if p.get("paper") else p['title']
    code_link = f"[Code]({p['code']})" if p.get("code") else ""
    project_link = f"[Project]({p['project']})" if p.get("project") else ""
    table += f"| {p['year']} | {title_link} | {', '.join(p['authors'])} | {p.get('modality','')} | {', '.join(p.get('tags',[]))} | {title_link} | {code_link} | {project_link} | {p.get('local_eval','')} |\n"

# 4. 同理处理 datasets.yml
# 5. 拼接 README 模板固定部分和动态表格
with open("../README.md", "w") as f:
    f.write("# 3DGS-SLAM Literature & Datasets\n\n")
    f.write("Open Website: [View Papers](https://github.com/sychina/awesome-3DGS-SLAM-and-Datasets/)\n\n")
    f.write("## Papers\n")
    f.write(table)