from experta import *
import schema


class ProjectType(Fact):
    type = Field(schema.Or("mobile app", "website", "design", "ai system"))


class TimeScope(Fact):
    time = Field(int, mandatory=True)


class Tools(Fact):
    tools = Field(schema.Or(
        "C++",
        "golang",
        "Javascript",
        "Java",
        "C#",
        "Rust",
        "React Native",
        "Swift",
        "Flutter",
        "Kotlin"
    ))


class Prototype(Fact):
    pr = Field(schema.Or(
        'yes', 'no'
    ))


class Requirements(Fact):
    n_req = Field(int, mandatory=True)

# tipe=mobile add cost_type=20000 and est_time=4
# tipe=web add cost_type=30000 and est_time=5
# tipe=ai add cost_type=40000 and est_time=8
# tipe=design add cost_type=50000 and est_time=2

# tech=flutter add raise=10% and exp=10
# tech=javascript add raise=10% and exp=10
# tech=python add raise=20% and exp=20
# tech=rust add raise=40% and exp=40
# tech=golang add raise=10% and exp=10
# tech=kotlin add raise=15% and exp=15

# time - est_time == 0 add raise_time=10%
# time - est_time > 0 add raise_time=0%
# time - est_time < 0 add raise_time=20%

# prototipe=ya add reduce_cost=5%
# prototipe=tidak add reduce_cost=0%

# n_req=val add extra_cost=val*100000


class ProjectCost(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.EXP = 0
        self.MIN_LEVEL = 0
        self.PAYMENT = 0

    @DefFacts()
    def _declare_initial_fact(self, tipe, tech, time, prototipe, n_req):
        yield Fact(tipe=tipe, time=time, tech=tech, prototipe=prototipe, n_req=n_req)

    @Rule(Fact(tipe='mobile'))
    def mobile_type(self):
        self.declare(Fact(est_time=4))
        self.declare(Fact(q1=True))
        self.declare(Fact(cost=2000000))

    @Rule(Fact(tipe='web'))
    def web_type(self):
        self.declare(Fact(est_time=5))
        self.declare(Fact(q1=True))
        self.declare(Fact(cost=4000000))

    @Rule(Fact(tipe='ai'))
    def ai_type(self):
        self.declare(Fact(est_time=8))
        self.declare(Fact(q1=True))
        self.declare(Fact(cost=3000000))

    @Rule(Fact(tipe='design'))
    def design_type(self):
        self.declare(Fact(est_time=2))
        self.declare(Fact(q1=True))
        self.declare(Fact(cost=200000))

    @Rule(Fact(tech='flutter'), Fact(q1=True))
    def flutter_tech(self):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(Fact(tech='javascript'), Fact(q1=True))
    def javascript_tech(self):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(Fact(tech='python'), Fact(q1=True))
    def python_tech(self):
        self.declare(Fact(raise_tech=20))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(Fact(tech='rust'), Fact(q1=True))
    def rust_tech(self):
        self.declare(Fact(raise_tech=40))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(Fact(tech='golang'), Fact(q1=True))
    def golang_tech(self):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(Fact(tech='kotlin'), Fact(q1=True))
    def kotlin_tech(self):
        self.declare(Fact(raise_tech=15))
        self.declare(Fact(exp=10))
        self.declare(Fact(q2=True))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time > est_time),
        Fact(q2=True)
    )
    def time_gt(self, time, est_time):
        self.declare(Fact(raise_time=0))
        self.declare(Fact(q3=True))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time < est_time),
        Fact(q2=True)
    )
    def time_lt(self, time, est_time):
        self.declare(Fact(raise_time=20))
        self.declare(Fact(q3=True))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time == est_time),
        Fact(q2=True)
    )
    def time_eq(self, time, est_time, raise_tech):
        self.declare(Fact(raise_time=10))
        self.declare(Fact(q3=True))

    @Rule(Fact(prototipe='ada'), Fact(q3=True))
    def prototipe_ada(self):
        self.declare(Fact(reduce_cost=5))
        self.declare(Fact(q4=True))
        # print('q3')

    @Rule(Fact(prototipe='tidak'), Fact(q3=True))
    def prototipe_tidak(self):
        self.declare(Fact(reduce_cost=0))
        self.declare(Fact(q4=True))

    @Rule(
        Fact(n_req=MATCH.n_req),
        TEST(lambda n_req: n_req > 0),
        Fact(q4=True),
        Fact(raise_time=MATCH.raise_time),
        Fact(raise_tech=MATCH.raise_tech),
        Fact(exp=MATCH.exp),
        Fact(reduce_cost=MATCH.reduce_cost),
        Fact(cost=MATCH.cost)
        # Fact(reduce_cost=MATCH.reduce_cost)
    )
    def n_requirement(self, n_req, raise_time, raise_tech, exp, reduce_cost, cost):
        total_raise = raise_tech + raise_time - reduce_cost
        level = exp*10 + n_req
        final_cost = cost*(1+total_raise/100) + n_req*(0.1)
        # print(f'{total_raise} {exp} {final_cost}')
        # return {level, exp, final_cost}
        # global EXP
        # global MIN_LEVEL
        # global PAYMENT
        self.EXP = exp
        self.MIN_LEVEL = level
        self.PAYMENT = final_cost
