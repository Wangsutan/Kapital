import matplotlib.pyplot as plt


def reproduce_m(vp, mgp, ccp, vrr, mr):
    return (vp + (mgp - ccp) * vrr) * mr


vp = 2000
mr = 0.50
mgp = vp * mr
ccp = 50
vrr = 0.25

m = reproduce_m(vp, mgp, ccp, vrr, mr)
print("for instance, reproduce surplus value once,\nm = %f" % m)


print("if ccp is increasing...")
ccp_list = [50 * i for i in range(0, int(vp / 50) + 1)]
m_list = [reproduce_m(vp, mgp, ccp, vrr, mr) for ccp in ccp_list]

plt.plot(ccp_list, m_list, label="m")
plt.legend()
plt.title("reproduce surplus value while $cc_p$ is increasing")
