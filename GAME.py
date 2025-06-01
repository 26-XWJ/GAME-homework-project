import tkinter as tk
from tkinter import messagebox, simpledialog
import random

MAX_STAGES = 5
MIN_MAKE = 1500
MAX_MAKE = 3000
MIN_PRICE, MAX_PRICE = 10, 30

# 阶段环境参数，customer_base为基数，price_coef为售价系数
STAGE_ENVIRONMENTS = [
    {
        "customer_base": 3500,
        "price_coef": 15,
        "cost_factor": 1.0,
        "desc": "春季来临，天气转暖，顾客稳定，成本正常。"
    },
    {
        "customer_base": 2750,
        "price_coef": 25,
        "cost_factor": 1.3,
        "desc": "炎热夏季，顾客价格敏感度高，成本上涨。"
    },
    {
        "customer_base": 2000,
        "price_coef": 30,
        "cost_factor": 1.5,
        "desc": "秋季竞争激烈，价格弹性大，成本高。"
    },
    {
        "customer_base": 3500,
        "price_coef": 18,
        "cost_factor": 0.7,
        "desc": "冬季促销季，顾客回升，成本降低。"
    },
    {
        "customer_base": 4500,
        "price_coef": 12,
        "cost_factor": 1.0,
        "desc": "春节旺季，顾客多，价格敏感度最低。"
    },
]

DAILY_KNOWLEDGE = [
    "经济学知识点：供需关系。售价越高，需求越低，找到平衡点至关重要。",
    "库存管理：库存过多浪费，库存过少损失销量，合理安排制作量。",
    "成本与利润：控制成本，保持合理售价，才能实现利润最大化。",
    "价格弹性：售价变动影响需求，夏季价格敏感度更高。",
    "风险管理：市场波动不可预测，保持应急资金安全运营。",
]

PUBLIC_ECON_QUESTIONS = [
    ("公共物品的典型特征是什么？\nA. 非排他性和非竞争性\nB. 有偿使用\nC. 个人所有", "A"),
    ("哪种税收方式能有效缓解贫富差距？\nA. 累进税制\nB. 固定税率\nC. 免税", "A"),
    ("外部性正面影响的例子是？\nA. 公共交通减少污染\nB. 垃圾乱扔\nC. 噪音污染", "A"),
    ("公共经济学主要研究？\nA. 政府如何有效配置资源\nB. 个人理财\nC. 股票市场", "A"),
    ("什么是“搭便车”问题？\nA. 利用公共物品不付费的行为\nB. 多付税款\nC. 提供私人服务", "A"),
]

class MilkTeaShopGame:
    def __init__(self, root):
        self.root = root
        self.root.title("奶茶店经营模拟游戏")
        self.root.geometry("700x650")
        self.money = 10000.0  # 初始资金
        self.stock = 0
        self.stage = 0
        self.price = 20
        self.cost_per_cup_base = 6.0
        self.running = False

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()
        self.root.config(bg="#f5e1da")

        title = tk.Label(self.root, text="奶茶店经营模拟游戏", font=("Comic Sans MS", 24, "bold"), bg="#f5e1da", fg="#4b3832")
        title.pack(pady=20)

        intro_text = (
            "欢迎来到奶茶店经营模拟！\n\n"
            "你是奶茶店老板，每个阶段决定奶茶制作数量和售价，\n"
            "面对变化的市场环境，努力赚取最多利润！\n\n"
            "经济学知识点包括：\n"
            "- 成本与收益平衡\n"
            "- 库存管理风险\n"
            "- 需求与价格的关系\n\n"
            f"游戏时长：{MAX_STAGES}个经营阶段\n"
            "目标：积累尽可能多的资金！\n\n"
            "操作说明：\n"
            f"输入你想制作的奶茶数量({MIN_MAKE}-{MAX_MAKE} 杯)和售价(10-30元)，点击“开始游戏”！"
        )
        intro = tk.Label(self.root, text=intro_text, font=("Arial", 13), bg="#f5e1da", fg="#333")
        intro.pack(pady=10)

        start_btn = tk.Button(self.root, text="开始游戏", font=("Arial", 14), bg="#9b5de5", fg="white", command=self.start_game)
        start_btn.pack(pady=20)

        self.root.after(300, lambda: self.show_knowledge_point(-1))

    def show_knowledge_point(self, stage_index):
        if stage_index == -1:
            msg = (
                "开始前知识点：\n\n"
                "经济学告诉我们，价格和需求密切相关，合理定价是奶茶店成功的关键。\n"
                "同时，库存管理也不可忽视，过多浪费，过少错失收益。祝你经营顺利！"
            )
        else:
            idx = stage_index % len(DAILY_KNOWLEDGE)
            msg = f"第 {stage_index+1} 阶段经营总结：\n\n{DAILY_KNOWLEDGE[idx]}"
        messagebox.showinfo("经济学知识点总结", msg)

    def start_game(self):
        self.money = 10000.0
        self.stock = 0
        self.stage = 1
        self.price = 20
        self.running = True
        self.create_game_screen()

    def create_game_screen(self):
        self.clear_screen()
        self.root.config(bg="#fff8f0")

        self.status_frame = tk.Frame(self.root, bg="#ffb4a2", height=80)
        self.status_frame.pack(fill=tk.X)

        self.stage_label = tk.Label(self.status_frame, text=f"阶段 {self.stage} / {MAX_STAGES}", font=("Arial", 18, "bold"), bg="#ffb4a2", fg="#6a4c93")
        self.stage_label.pack(side=tk.LEFT, padx=15, pady=20)

        self.money_label = tk.Label(self.status_frame, text=f"资金：{self.money:.2f} 元", font=("Arial", 16), bg="#ffb4a2", fg="#222")
        self.money_label.pack(side=tk.LEFT, padx=15)

        self.stock_label = tk.Label(self.status_frame, text=f"库存：{self.stock} 杯", font=("Arial", 16), bg="#ffb4a2", fg="#222")
        self.stock_label.pack(side=tk.LEFT, padx=15)

        self.price_label = tk.Label(self.status_frame, text=f"当前售价：{self.price} 元/杯", font=("Arial", 16), bg="#ffb4a2", fg="#222")
        self.price_label.pack(side=tk.LEFT, padx=15)

        input_frame = tk.Frame(self.root, bg="#fff8f0")
        input_frame.pack(pady=15)

        tk.Label(input_frame, text=f"奶茶制作数量 ({MIN_MAKE}-{MAX_MAKE} 杯):", font=("Arial", 14), bg="#fff8f0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.make_entry = tk.Entry(input_frame, font=("Arial", 14), width=10)
        self.make_entry.grid(row=0, column=1, pady=5)
        self.make_entry.insert(0, str(MIN_MAKE))

        tk.Label(input_frame, text="售价 (10-30 元/杯):", font=("Arial", 14), bg="#fff8f0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.price_entry = tk.Entry(input_frame, font=("Arial", 14), width=5)
        self.price_entry.grid(row=1, column=1, pady=5)
        self.price_entry.insert(0, str(self.price))

        self.confirm_button = tk.Button(input_frame, text="确认本阶段经营", font=("Arial", 14), bg="#6a4c93", fg="white", command=self.play_stage)
        self.confirm_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 需求函数显示区域，突出醒目
        demand_frame = tk.Frame(self.root, bg="#fff0d4", bd=4, relief=tk.SOLID)
        demand_frame.pack(pady=15, fill=tk.X, padx=20)

        demand_title = tk.Label(demand_frame, text="当前阶段需求函数", font=("Arial", 18, "bold"), bg="#fff0d4", fg="#b36100")
        demand_title.pack(pady=(8, 0))

        self.demand_label = tk.Label(demand_frame, text="", font=("Consolas", 20, "bold"), bg="#fff0d4", fg="#a64c00", justify=tk.LEFT)
        self.demand_label.pack(padx=15, pady=10)

        # 说明
        self.demand_desc_label = tk.Label(demand_frame, text="", font=("Arial", 12), bg="#fff0d4", fg="#7a4700", justify=tk.LEFT)
        self.demand_desc_label.pack(padx=15, pady=(0,8))

        log_frame = tk.LabelFrame(self.root, text="经营日志与反馈", font=("Arial", 14), fg="#6a4c93", bg="#fff8f0", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.log_text = tk.Text(log_frame, font=("Consolas", 12), bg="#f0e7f5", fg="#333", state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.update_stage_info()

    def update_stage_info(self):
        env = STAGE_ENVIRONMENTS[self.stage - 1]
        self.stage_label.config(text=f"阶段 {self.stage} / {MAX_STAGES}")
        self.money_label.config(text=f"资金：{self.money:.2f} 元")
        self.stock_label.config(text=f"库存：{self.stock} 杯")
        self.price_label.config(text=f"当前售价：{self.price} 元/杯")

        # 需求函数具体数字表达，类似 Q = 3500 - 15 × 价格
        formula_text = f"需求量 = {env['customer_base']} - {env['price_coef']} × 价格（元）"
        self.demand_label.config(text=formula_text)
        self.demand_desc_label.config(text=f"市场环境描述:\n{env['desc']}")

    def play_stage(self):
        try:
            make_count = int(self.make_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字。")
            return

        if not (MIN_MAKE <= make_count <= MAX_MAKE):
            messagebox.showerror("输入错误", f"制作数量应在{MIN_MAKE}至{MAX_MAKE}之间。")
            return
        if not (MIN_PRICE <= price <= MAX_PRICE):
            messagebox.showerror("输入错误", f"售价应在{MIN_PRICE}至{MAX_PRICE}元之间。")
            return

        env = STAGE_ENVIRONMENTS[self.stage - 1]
        cost_per_cup = self.cost_per_cup_base * env["cost_factor"]
        total_cost = cost_per_cup * make_count

        if total_cost > self.money:
            messagebox.showerror("资金不足", f"资金不足支付成本：需要{total_cost:.2f}元，当前资金{self.money:.2f}元。")
            return

        self.price = price
        self.stock = make_count
        self.money -= total_cost

        # 实际需求 = customer_base - price_coef × price，保底0，且随机上下波动±5%
        base_demand = env["customer_base"] - env["price_coef"] * price
        fluctuation = random.uniform(0.95, 1.05)
        demand = max(0, int(base_demand * fluctuation))

        sales = min(demand, self.stock)

        revenue = sales * price
        self.money += revenue
        self.stock -= sales

        self.append_log(f"阶段 {self.stage} 经营总结：")
        self.append_log(f"制作奶茶：{make_count} 杯，售价：{price:.2f} 元/杯")
        self.append_log(f"预估需求量（含波动）：{demand} 杯，实际售出：{sales} 杯")
        self.append_log(f"成本支出：{total_cost:.2f} 元，收入：{revenue:.2f} 元")
        self.append_log(f"库存剩余：{self.stock} 杯，资金余额：{self.money:.2f} 元\n")

        self.show_knowledge_point(self.stage - 1)

        self.stage += 1
        if self.stage > MAX_STAGES:
            self.end_game()
        else:
            self.update_stage_info()
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, str(MIN_MAKE))
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(self.price))

    def append_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def end_game(self):
        self.running = False
        self.append_log("游戏结束！")
        self.append_log(f"最终资金余额：{self.money:.2f} 元")
        self.append_log("感谢游玩！")

        self.show_public_econ_quiz()

    def show_public_econ_quiz(self):
        score = 0
        for i, (q, ans) in enumerate(PUBLIC_ECON_QUESTIONS):
            user_ans = simpledialog.askstring(f"公共经济学问答 {i+1}", q)
            if user_ans is None:
                messagebox.showinfo("答题结束", "答题中断。")
                break
            if user_ans.strip().upper() == ans:
                score += 1
                messagebox.showinfo("回答正确", "回答正确！")
            else:
                messagebox.showinfo("回答错误", f"回答错误。正确答案是：{ans}")

            # 最后题答对奖励
            if i == len(PUBLIC_ECON_QUESTIONS) - 1 and user_ans.strip().upper() == ans:
                messagebox.showinfo("奖励！", "恭喜答对最后一道题！获得额外1000元奖励！")
                self.money += 1000

        messagebox.showinfo("问答结束", f"公共经济学问答结束，得分：{score} / {len(PUBLIC_ECON_QUESTIONS)}")

        self.create_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MilkTeaShopGame(root)
    root.mainloop()
