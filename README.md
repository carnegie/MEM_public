# MEM_public/Henry_et_al_2020

This specific branch documents the state of MEM used for the inter-model comparison project: https://github.com/carnegie/mem commit 645688243118e01645d38576a1cbe94104bf4808

The `Input_Data/` directory is empty by default and must be populated with input files
tracked in the inter-model comparison repository: https://github.com/carnegie/capacity-expansion-model-intercomparison/

## Add some instructions on how to do this?



## MEM = Macro Energy Model
A collaborative project hosted by Carnegie Institution for Science.
Ken Caldeira <kcaldeira@carnegiescience.edu>


Python 3.7 (or 3.6!) and cvxpy 1.x version of MEM 2. This is a Macro Energy Model that optimizes electricity (or electricity
and fuels) without considering any spatial variation, policy, capacity markets, etc.

Currently, the technologies considered in this release of MEM 2, and their associated keywords, are:


    tech_keywords['demand'] = ['tech_name','tech_type','node_from','series_file','normalization']
    tech_keywords['curtailment'] = ['tech_name','tech_type','node_from','var_cost']
    tech_keywords['lost_load'] = ['tech_name','tech_type','node_to','var_cost']
    tech_keywords['generator'] = ['tech_name','tech_type','node_to','series_file','fixed_cost','var_cost','normalization','capacity']
    tech_keywords['fixed_generator'] = ['tech_name','tech_type','node_to','series_file','fixed_cost','normalization','capacity']
    tech_keywords['transfer'] = ['tech_name','tech_type','node_to','node_from','fixed_cost','var_cost','efficiency','capacity']
    tech_keywords['transmission'] = ['tech_name','tech_type','node_to','node_from','fixed_cost','var_cost','efficiency','capacity']
    tech_keywords['storage'] = ['tech_name','tech_type','node_to','node_from','fixed_cost','var_cost','efficiency','charging_time','decay_rate','capacity']

For a full list of input variables, it is best to look inside <Preprocess_Input.py>.

<br>
<b>=====  WINDOWS 10 INSTALLATION INSTRUCTIONS  ===== </b>
<br>
The following is installation instructions for Windows 10 machines.

1. Install Anaconda3. https://www.anaconda.com/download/ https://conda.io/docs/user-guide/install/windows.html

2. Install Visual C++ 14.0. Download and install software using this link. https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15 See this link for more information: https://www.scivision.co/python-windows-visual-c++-14-required/

3. Download and install Gurobi. http://www.gurobi.com/documentation/8.0/quickstart_windows/quickstart_windows.html http://www.gurobi.com/documentation/8.0/quickstart_windows/creating_a_new_academic_li.html#subsection:createacademiclicense

4. Activate Gurobi license. You have to go to this page https://user.gurobi.com/download/licenses/current to see what licenses are allocated to you. Click on the license that will pertain to your machine. A window will open up that will have some text like:

		grbgetkey #############################

Copy that text and paste in in an Anaconda window.

5. Set up Python link to Gurobi. Open up the Anaconda3 window as Administrator from the Start Menu and then type:

	       > cd  c:/gurobi811/win64
	       > python setup.py install
	       
If this install fails on installing, try the following line in an Anaconda window:

	       > conda config --add channels http://conda.anaconda.org/gurobi
	       > conda install gurobi

6. Install cvxpy. For Python3, cvxpy must be installed with pip. Open up an Anaconda window and type:

	       > pip install cvxpy 

If this install fails on installing the ecos package, try the following line in an Anaconda window:

	       > install ecos
	       > pip install cvxpy

<b>Additional notes on installing cvxpy</b>

If you get error messages for not having (or not having the correct versions of) ecos, scs, or cvxcanon, try the following command (<a href="https://anaconda.org/sebp/cvxpy">Anaconda Cloud</a>): 

	       > conda install -c sebp cvxpy

This command should automatically install the right packages needed for cvxpy ("-c CHANNEL" specifies additional channels to search for packages; sebp is a contributer on Anaconda Cloud).

Check the installation with:

	       > nosetests cvxpy 

7. Download and run Python3 version of the Macro Energy Model:
-- Open case_input.xlsx in Excel. Make the cases you want and then save sheet as case_input.csv.
-- Open Spyder and then within Spyder navigate to the folder that was cloned from Github and open and run Macro_Energy_Model.py.


<br>
<b>=====  MacOS 10.13 INSTALLATION INSTRUCTIONS  ===== </b>
<br>
The following is installation instructions for MacOS 10.13 machines.

1. Install Anaconda3 for MacOS. https://www.anaconda.com/download/

2. Download and install Gurobi. http://www.gurobi.com/downloads/download-center  http://www.gurobi.com/downloads/gurobi-optimizer

3. Activate the Gurobi license. You have to go to this page https://user.gurobi.com/download/licenses/current to see what licenses are allocated to you. Click on the license that will pertain to your machine. A window will open up that will have some text like:

	grbgetkey ##################

4. Copy that text and paste it in an Anaconda terminal window.

5. Set up Python link to Gurobi. Open up the Anaconda3 terminal window as Administrator from the Start Menu and then type:

	       > conda config --add channels http://conda.anaconda.org/gurobi	
	       > conda install gurobi

6. Install cvxpy. For Python3, cvxpy must be installed with pip. Open up an Anaconda window and type:

	       > pip install cvxpy 

7. If you get error messages for not having (or not having the correct versions of) ecos, scs, or cvxcanon, try the following command (Anaconda Cloud):

	       > conda install -c sebp cvxpy

This command should automatically install the right packages needed for cvxpy ("-c CHANNEL" specifies additional channels to search for packages; sebp is a contributer on Anaconda Cloud).

Check the installation with:

	       > nosetests cvxpy 

If you did not remove an old Gurobi license and installed a new one, you might see an error in this step. You need to delete the old Gurobi licencse and install the new one for your current Gurobi version.

8. Download and run Python3 version of the Macro Energy Model
-- Open case_input.xlsx in Excel. Make the cases you want and then save sheet as case_input.csv.
-- Open Spyder and then within Spyder navigate to the folder that was cloned from Github and open and run Macro_Energy_Model.py.
