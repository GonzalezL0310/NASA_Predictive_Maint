Technical Assessment: Unit 1 Sensor Response and Degradation Dynamics

![Análisis de Degradación del Motor 1](reports/figures/unit_1_analysis.png)

- Thermodynamic Coupling and Compensation: Telemetry for LPT_Outlet_Temp (T_50) exhibits a persistent upward drift, rising from ∼1400 to >1425 units. This temperature shift is a direct result of the closed-loop control system compensating for adiabatic efficiency loss in the High-Pressure Compressor (HPC). To maintain the target thrust, the fuel-to-air ratio is adjusted, subsequently increasing the enthalpy and temperature of the exhaust gases.

- HPC Health Indicators: The downward trend in HPC_Outlet_Press (P_30), falling from 554.5 to 551 psia, serves as a primary indicator of component structural health. The observed loss in compression capacity is consistent with physical degradation mechanisms such as airfoil erosion or increased tip clearances. The divergence between decreasing pressure (bottom plot) and increasing temperature (top plot) validates a localized degradation event within the gas path.

- Unstable Damage Propagation: Both signals demonstrate a marked increase in the red dashed line (Slope) post-cycle 175. This validates the capturing of exponential damage propagation, where the wear rate accelerates significantly as the subsystem nears its operational limit, modeled by the health index h(t)=1−exp{atb}. Termination occurs at cycle 192, precisely when the normalized Health Index reaches zero due to breached operability margins.

- Signal-to-Noise Ratio and Processing: The high variance in the green line (Raw) reflects a multi-stage noise model—incorporating initial manufacturing variations, operational process noise, and sensor measurement stochasticity. The integration of the blue line (Moving Average) in your ETL pipeline is critical; it recovers the latent physics from the contaminated signal, revealing the smooth degradation trajectory that is otherwise masked by the jagged raw data.

By aligning the Slope on a twin axis, the visualization now clearly shows that the "speed" of degradation isn't constant; it is accelerating, which is the "smoking gun" for a non-linear failure model. While Unit 1 demonstrates these specific trends, the exact point of failure and noise distribution may vary in other units depending on the initial deterioration parameters and stochastic noise defined in the simulation.

