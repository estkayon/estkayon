<!-- ===================== ANIMATED HEADER ===================== -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=220&section=header&text=Md%20Estiak%20Rahman%20Ayon&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=34&desc=ML%20%7C%20MLOps%20%7C%20Full-Stack&descAlignY=54&descSize=18" width="100%" />

<!-- ===================== TYPING ANIMATION ===================== -->
<p align="center">
  <a href="https://github.com/estkayon">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=00D9FF&center=true&vCenter=true&width=620&lines=Machine+Learning+Engineer;MLOps+%26+Pipeline+Automation;Full-Stack+Developer;Data+Visualization+Enthusiast;Always+learning+something+new" alt="Typing SVG" />
  </a>
</p>

<!-- ===================== SOCIALS ===================== -->
<p align="center">
  <a href="https://www.linkedin.com/in/md-estiak-rahman-ayon/"><img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:estiakayon@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://www.facebook.com/estiak.ayon99"><img src="https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white" alt="Facebook"></a>
  <a href="https://www.instagram.com/_ayooonx7/"><img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white" alt="Instagram"></a>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=estkayon&label=Profile%20views&color=00D9FF&style=flat-square" alt="Profile views" />
  <img src="https://img.shields.io/github/followers/estkayon?label=Followers&style=flat-square&color=00D9FF" alt="Followers" />
</p>

---

## 🧑‍💻 About Me

```python
class Ayon:
    def __init__(self):
        self.role     = "ML Engineer / MLOps"
        self.location = "Dhaka, Bangladesh"
        self.learning = ["Kubeflow", "Model Monitoring", "System Design"]
        self.stack    = ["Python", "PyTorch", "Docker", "Kubernetes", "FastAPI"]

    def say_hi(self):
        print("Thanks for dropping by! Let's build something together.")


me = Ayon()
me.say_hi()
```

> _Edit the values above — they're placeholders, not facts about you._

---

## ⚙️ MLOps

The part of ML that isn't the model: getting it into production and keeping it healthy there.

```mermaid
flowchart LR
    A[Data Collection] --> B[Data Versioning<br/>DVC]
    B --> C[Experimentation<br/>MLflow]
    C --> D[Training Pipeline<br/>Airflow]
    D --> E[Model Registry<br/>MLflow]
    E --> F[CI/CD<br/>GitHub Actions]
    F --> G[Serving<br/>FastAPI + Docker + K8s]
    G --> H[Monitoring<br/>Prometheus + Grafana]
    H --> |Drift detected| D
```

<details>
<summary><b>📋 What each stage covers (click to expand)</b></summary>

<br>

| Stage | Purpose | Tools |
|---|---|---|
| Data versioning | Reproducible datasets tied to each commit | DVC, Git LFS |
| Experiment tracking | Compare runs, params, metrics, artifacts | MLflow |
| Orchestration | Scheduled, retryable training pipelines | Apache Airflow |
| Packaging | Reproducible environments and images | Docker, Conda |
| CI/CD | Test, build and deploy on every merge | GitHub Actions, GitLab CI |
| Serving | Low-latency inference endpoints | FastAPI, Kubernetes |
| Monitoring | Latency, throughput, data & concept drift | Prometheus, Grafana |

**Practices I follow**

- Every experiment is reproducible: pinned dependencies, versioned data, logged seeds
- Models are promoted through a registry (staging → production), never copied by hand
- Training and serving share the same preprocessing code to avoid train/serve skew
- Rollback is a one-command operation, and monitoring decides when to retrain

</details>

<p align="center">
  <img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white" />
  <img src="https://img.shields.io/badge/DVC-13ADC7?style=for-the-badge&logo=dvc&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white" />
  <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white" />
  <img src="https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white" />
</p>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,2,2,5,30&height=3" width="100%" />

## 💻 Tech Stack

<details open>
<summary><b>Languages</b></summary>
<br>

![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![C#](https://img.shields.io/badge/c%23-%23239120.svg?style=for-the-badge&logo=csharp&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)

</details>

<details>
<summary><b>Machine Learning & Data</b></summary>
<br>

![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Power BI](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

</details>

<details>
<summary><b>Web & Frameworks</b></summary>
<br>

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Node.js](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Laravel](https://img.shields.io/badge/laravel-%23FF2D20.svg?style=for-the-badge&logo=laravel&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%237952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)

</details>

<details>
<summary><b>Databases, Tools & Design</b></summary>
<br>

![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23FC6D26.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![OpenGL](https://img.shields.io/badge/OpenGL-%235586A4.svg?style=for-the-badge&logo=opengl&logoColor=white)
![Cisco](https://img.shields.io/badge/cisco-%23049fd9.svg?style=for-the-badge&logo=cisco&logoColor=black)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)
![Lightroom](https://img.shields.io/badge/Adobe%20Lightroom-31A8FF.svg?style=for-the-badge&logo=adobelightroom&logoColor=white)
![Premiere Pro](https://img.shields.io/badge/Adobe%20Premiere%20Pro-9999FF.svg?style=for-the-badge&logo=adobepremierepro&logoColor=white)

</details>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,2,2,5,30&height=3" width="100%" />

## 📊 GitHub Stats

<p align="center">
  <img width="49%" src="https://github-readme-stats.vercel.app/api?username=estkayon&show_icons=true&theme=tokyonight&hide_border=true&include_all_commits=true&count_private=true" alt="GitHub stats" />
  <img width="41%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=estkayon&theme=tokyonight&hide_border=true&layout=compact&langs_count=8" alt="Top languages" />
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com/?user=estkayon&theme=tokyonight&hide_border=true" alt="GitHub streak" />
</p>

### 🏆 Trophies

<p align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=estkayon&theme=tokyonight&no-frame=true&no-bg=true&column=7&margin-w=6&margin-h=6" alt="Trophies" />
</p>

### 📈 Contribution Activity

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=estkayon&theme=tokyo-night&hide_border=true&area=true&custom_title=Contribution%20Graph" alt="Activity graph" width="100%" />
</p>

### 🐍 Watch the snake eat my contributions

<p align="center">
  <img src="https://raw.githubusercontent.com/estkayon/estkayon/output/snake.svg" alt="Snake animation" />
</p>

> ⚠️ The snake only shows up after you add the `snake.yml` workflow and run it once — see the setup notes.

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,2,2,5,30&height=3" width="100%" />

## 📌 Featured Projects

<p align="center">
  <a href="https://github.com/estkayon/REPO-ONE">
    <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=estkayon&repo=REPO-ONE&theme=tokyonight&hide_border=true" />
  </a>
  <a href="https://github.com/estkayon/REPO-TWO">
    <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=estkayon&repo=REPO-TWO&theme=tokyonight&hide_border=true" />
  </a>
</p>

> Replace `REPO-ONE` and `REPO-TWO` with your actual repository names.

---

## 💡 Dev Quote of the Day

<p align="center">
  <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight" alt="Random dev quote" />
</p>

## 😄 Random Dev Joke

<p align="center">
  <img src="https://readme-jokes.vercel.app/api?theme=tokyonight&hideBorder" alt="Jokes card" />
</p>

---

<p align="center">
  <b>Thanks for visiting! Feel free to ⭐ a repo or say hello.</b>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=140&section=footer" width="100%" />
