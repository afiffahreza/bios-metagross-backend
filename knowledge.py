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
    @DefFacts()
    def _declare_initial_fact(self, tipe, tech, time, proto, n_req):
        yield Fact(tipe=tipe, time=time, tech=tech, proto=proto, n_req=n_req)

    @Rule(Fact(tipe='mobile'))
    def mobile_type(self):
        self.declare(Fact(est_time=4))
        print('mobile')

    @Rule(Fact(tipe='web'))
    def web_type(self):
        self.declare(Fact(est_time=5))
        print('web')

    @Rule(Fact(tipe='ai'))
    def ai_type(self):
        self.declare(Fact(est_time=8))
        print('ai')

    @Rule(Fact(tipe='design'))
    def design_type(self):
        self.declare(Fact(est_time=2))

    @Rule(Fact(tech='flutter'), Fact(tipe=MATCH.tipe))
    def flutter_tech(self, tipe):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))

    @Rule(Fact(tech='javascript'), Fact(tipe=MATCH.tipe))
    def javascript_tech(self, tipe):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))

    @Rule(Fact(tech='python'), Fact(tipe=MATCH.tipe))
    def python_tech(self, tipe):
        self.declare(Fact(raise_tech=20))
        self.declare(Fact(exp=10))

    @Rule(Fact(tech='rust'), Fact(tipe=MATCH.tipe))
    def rust_tech(self, tipe):
        self.declare(Fact(raise_tech=40))
        self.declare(Fact(exp=10))

    @Rule(Fact(tech='golang'), Fact(tipe=MATCH.tipe))
    def golang_tech(self, tipe):
        self.declare(Fact(raise_tech=10))
        self.declare(Fact(exp=10))

    @Rule(Fact(tech='kotlin'), Fact(tipe=MATCH.tipe))
    def kotlin_tech(self, tipe):
        self.declare(Fact(raise_tech=15))
        self.declare(Fact(exp=10))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time > est_time)
    )
    def time_gt(self, time, est_time):
        self.declare(Fact(raise_time=0))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time < est_time)
    )
    def time_lt(self, time, est_time):
        self.declare(Fact(raise_time=20))

    @Rule(
        Fact(time=MATCH.time),
        Fact(est_time=MATCH.est_time),
        TEST(lambda time, est_time: time == est_time)
    )
    def time_eq(self, time, est_time, raise_tech):
        self.declare(Fact(raise_time=10))

    @Rule(Fact(prototipe='ada'))
    def prototipe_ada(self):
        self.declare(reduce_cost=5)

    @Rule(Fact(prototipe='tidak'))
    def prototipe_tidak(self):
        self.declare(reduce_cost=0)

    @Rule(
        Fact(n_req=MATCH.n_req),
        TEST(lambda n_req: n_req > 0),
        # Fact(reduce_cost=MATCH.reduce_cost)
    )
    def n_requirement(self, n_req):
        # self.declare(extra_cost=10*n_req)
        # print('mantapS')
        # print(self.strategy)
        # print(self.facts)
        # print(self.facts)

        for f in self.facts:
            print(f)


engine = ProjectCost()
engine.reset(tipe='ai', time=20, tech='flutter', proto='ada', n_req=10)
engine.run()
# print(engine.result)
