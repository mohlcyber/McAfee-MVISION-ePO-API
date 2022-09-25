# McAfee-MVISION-ePO-API
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

These are simple scripts (examples) how to download Threat Events from the McAfee MVISION ePO and McAfee MVISION Mobile.

```
usage: python3 mvision_epo_events.py -R <Region> -U <User> -M <Minutes> -L <Limit> -F <File>

McAfee MVISION EPO Events Pull

optional arguments:
  -h, --help            show this help message and exit
  --region {US,SI,EU,SY}, -R {US,SI,EU,SY}
                        McAfee MVISION Tenant Region
  --user USER, -U USER  McAfee MVISION EPO Username
  --pw PW, -P PW        McAfee MVISION EPO Password
  --minutes MINUTES, -M MINUTES
                        Pull MVISION EPO Events from the last x Minutes
  --limit LIMIT, -L LIMIT
                        Maximum Events to retrieve
  --file {Y,N}, -F {Y,N}
                        Write output to file
```

Other scopes can be defined. Examples:

epo.admin epo.adit.r epo.qery.g epo.resp.ru epo.pevt.r epo.ubp.r epo.sdlr.r epo.dir.a epo.evt.r epo.dxlc.r epo.eagt.r epo.eagt.tr epo.dash.r ens.comn.r ens.comn.vs ens.fw.r ens.fw.vc ens.fw.vr ens.fw.vp ens.fw.vs ens.wp.tr ens.wp.r ens.wp.vs ens.atp.vs ens.atp.r ens.am.r ens.am.tr ens.am.vs ens.am.ve ens.vrs.r ens.vrs.tr mvs.endp.r epo.reg_token
