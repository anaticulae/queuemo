# Changelog

Every noteable change is logged here.

## v1.4.1

### Feature

* use new bib decider (ddfb1f5192ab)
* publish extracted bib to display to user (74986576e12d)

### Fix

* add missing input resource (00fb4b321358)

## v1.4.0

### Feature

* add smarty run and decide step (ed68ca908aee)
* add required docref step (6a9baa3de67f)

## v1.3.3

### Feature

* add decider links step (d326678c21f7)

## v1.3.2

## v1.3.1

## v1.3.0

### Feature

* add verbose flag (ce4c9d9ac5ec)
* run queuemo in single folder (3b784acf62d6)
* add basic single runtime infrastructure (167b8140f68c)

## v1.2.3

## v1.2.2

### Fix

* words is already done for magic (0fa5f434767a)
* add missing page shrink (c473e937df8c)

## v1.2.1

## v1.2.0

### Feature

* publish log after completing document (a3cbbba7f8c4)
* add --interactive flag to manually step thru execution (797205147a58)
* add method to ask user for continuing (c2bd72c4ab9f)

## v1.1.1

## v1.1.0

### Feature

* log start of ComposedRecipe (0c041d2fe26d)
* add magic step to run computation only once (d376ea24007a)

### Fix

* remove non existing validation step from scheduler (aa01ed9768e8)
* ensure that `ORDER` is used when for process scheduling (3f8d455fc85f)
* add missing input resources (a0e5688a7efe)

## v1.0.4

## v1.0.3

### Feature

* copy caption data to result view (cfe84f39c283)
* add verbose error logging (b8da0444c5dd)

## v1.0.2

## v1.0.1

## v1.0.0

### Feature

* remove outdated result value (ab52ea08305c)
* add profiling step to determine pdf analyzing time (af3dfcc4519d)

### Fix

* avoid copy findings twice (77da1824599f)
* simplify output path (a06272a1413b)

## v0.8.0

### Feature

* add imgfig runnable to analyze quality of images/figures (1fab0f074429)
* log version of used runnable (c050f8dbf365)
* add caption and formula extraction as magic data source (02cbf6ddbb5b)

### Fix

* do not start deleted jobs (fedf36a3cfe2)
* adjust step logging (b553cee266bd)
* add missing quotes extraction (20729f0ec740)

## v0.7.4

### Feature

* highlight start of recipe (ad9d654bbedb)

### Fix

* information (a670ce0cff21)

## v0.7.3

### Feature

* run new figure step (3fcd18cde16f)

### Fix

* skip non necessary step (5daed63ef9fe)

## v0.7.2

## v0.7.1

### Feature

* support merging multiple areas (10987bcfae92)
* add bibliography runnable to extract and judge bibliography (69597efd5e50)

### Documentation

* fix spelling content error (f3cd1780f9ec)

## v0.7.0

### Feature

* simplify pages pattern (a1011c2aef05)
* log path information in debug mode for every recipe step (52dc46a4e043)
* shrink feature analysis to expected areas (55b7c0a9a9cf)
* select toc and titlepage based on sections extractor (90b2d39db6dd)
* add sections step to determine location of potential toc etc (b6affc68d8c6)
* use rawmaker all flag to make interface robust against changes (6f46bd5fa7f6)

### Fix

* run sections once (bbb2fb50f6cc)
* ensure to have unique log file (ee3b664aea37)
* add missing test data generation after changing generator (00c683f65d8c)

## v0.6.4

### Fix

* inform about missing resource (608e84ab7566)

## v0.6.3

### Feature

* extend title page collector to more than page zero (871e1920bf3a)
* add method to log cli output to file (e0a5818c78b0)

## v0.6.2

### Feature

* beautify input paths (28dff947d9f4)

### Fix

* copy missing data (e758650bfe4e)

## v0.6.1

## v0.6.0

### Feature

* copy font information to resolve hashes in doctextstyle (8940a8a205f5)
* add content text style linter (8eb466f846f0)
* publish detected text style master (cf3ae8b94e79)
* add decider_textstyle to judge document headline style (85fa7fb66676)
* add footnote step to verify footnotes in footer (7800359e038f)
* run groupme at start once (7d0c6a8402b9)

### Fix

* always start on a new line (a0d33dbabcd2)

## v0.5.2

### Fix

* decrease job count only when job was successfully selected (44331b9b9038)

## v0.5.1

### Feature

* add second counter to determine ending of scheduler (11308719f8e3)

## v0.5.0

### Feature

* public words sentence result (1e2eef4e7ff9)
* reduces executed steps (fee27e31f809)
* enable converting boolean to flag (4a0a33274d4a)
* add textflow decider to runnable (0072c82fcc98)
* reduce startup time and remove duplicated code (4a3e1bb300f0)
* run groupme with multiple processes (fd5c03fc3bd8)
* run rawmaker extractor in parallel (13961e541ed7)
* add textflow validation and publishing step (eebb29ca0816)
* extract images and publish (ec2d840647b5)

### Fix

* enable required analysis (12186ef4afb8)
* do not copy cause rawmaker supports inpath without file ext (5e154c1b920b)
* use new rawmaker feature and access file directly (58027cbe5b4a)

## v0.4.3

### Feature

* run rawmaker oneline configuration for decider module (fa06d3bb3809)
* add border distance check to result view (13839a84bd67)
* make publish step selectable (f49914f64de6)
* add copy method which supports logging copy-operations (9e1b0837e7ae)
* add __str__ to extend debugging facility (bd47f15e1606)
* add toc validator to fast view analysis (de77d95597df)

### Fix

* put border validation results to correct folder (8e1b14a98034)

## v0.4.2

### Feature

* extract and present whole document (bb2f256d72fa)
* publish linter results to result view also (d75ed89baee2)
* reduce runtime of rawmaker application (b55e35df6903)

## v0.4.1

### Fix

* do not start a job twice (22126a72fc35)

## v0.4.0

### Feature

* add separate publish step (76bb4df0bb3e)
* extend runnable checker (5fc74460f082)
* add method to publish todo to ready folder (64a75cc00dc9)
* activate result scheduling step (41241ea9dba7)
* use oneline parameter to improve extraction result (ac9e4d4cff9f)
* extend recipes API (6bc61d4d2929)
* add new result view (7f4027ace2e3)
* add validation step to check that input resource is valid (80c11dfd1827)
* use new scheduling to run fastview (89e0c845330d)
* add runtime to run and manage schedules (51d2c3566c81)
* add recipe scheduler and two recipe examples (db81a1278de7)
* extend list with application test at startup (72e08439b9f3)

### Fix

* add required result folder (5bcfad455d1d)
* run validation task first (c5c7e934e663)
* set output path to todo path (5fa0130d894a)
* fix scheduling order (8e463c6de8e3)

### Documentation

* improve general documentation (edd6598d808e)
* extend interface documentation (df6a161103c4)
* extend interface documentation (5e43ad4ab2e4)
* extend module documentation (dfaf668ca897)

## v0.3.2

### Fix

* correct path where result html view must be stored (057d3d1768a5)

## v0.3.1

### Feature

* add mechanism to generate annotated pages (f94071ff2f4e)

### Fix

* create folder which must be create by feedback tool (e7b58fbefdd4)

### Documentation

* format docs (a5ebb0a9ca1c)
* Happy New Year! (a9a2e3810d25)
* update strategy documentation (5b35e46ca4db)

## v0.3.0

### Feature

* add resultview to scheduler (09019cdab667)
* add result view to invoke generation of resultview (0a4053361932)
* add verify and fastview step to scheduler (4281c8420848)
* add validation step to verify given pdf file (3bd7469fa300)
* add run step to run fastview recipe with sub-recipes (1f74c8db1fb7)
* add method to publish fast view results (a7e8f52c8d1d)
* add recipe to verify title page (576f89d9c224)
* extend file creation counter with file ending (67c79a0206e4)
* add method to extract required fastview resources (4a1eff62a4f7)

### Fix

* pass workspace result to job info (67daefce0da3)

### Documentation

* extend interface documentation (1af255b03e7f)
* introduce general doc structure (2e15f0ccafc6)

## v0.2.1

### Feature

* add method to display environment variables (65eabced70f5)
* setup logging level on start up via --verbose level (8f7c07b49ae0)
* show path which hits the assertion (728b68f3274d)
* add method to run command with manipulated os env (f507243895e5)
* add log entree of todo path after startup (6d7efd78a58d)

### Fix

* fix env vars - overwrite instead of replacing (9ac786b55ac0)
* ignore single file as working input (a85490be4137)
* close scheduler with correct error code on failure (ebdd73d4f7b7)
* fix typo in command line interface (e513b7e131f9)
* add missing package url (be6f1a7cd250)

## v0.2.0

### Feature

* use new featurepack multi input behavior (fa3f7696fa63)
* add generation of common view to display document (5b3a86b6c44d)
* add component to split document in different `Sections` (ef18e4268507)
* parameterize rawmaker to extract different layouts (98b92c8487ad)
* add optional args and prefix parameter to process runner (26cd8ba9562e)
* add new `recipe` approach (b08e985fc591)
* print invalid input error message and return failure (b5e857f38ef0)
* add loading file and accept comments (86c303f5ed26)
* add file to describe result view (243e052f2c3c)
* add tabstructure to simplify managing output paths (e915b70f545d)
* add method to copy files and folder (db08bc1d7257)

### Fix

* fix method header to pass kwargs to parametrize runnable s (d1ae5e70df9a)
* create all required parent folder (8e2e5f011b8d)

## v0.1.2

### Fix

* fix in/out path to new featurepack pattern (fc66a8e6a080)

## v0.1.1

### Feature

* add folder to store different recipes (34ce9ef8a827)
* add ugly font detection to default recipe (ccf09cf2c003)
* improve writing recipes - reduce code, improve stability (b2a4ad61ff74)

### Fix

* remove unit from result file, it is displayed by `viewo` (7fb87340bdd6)

## v0.1.0

### Feature

* remove temp path after finish and coping analysis (7d49e9463088)
* mark job as in progress with 0 percent (ae1235079635)
* extend logging of recipe process (797463a7d767)
* log version of used tools while startup process (7d4459b56131)
* add verbose flag to control verbosity of output (1ca679efb31d)
* add flags to control runtime of scheduler (23447a2a7fc4)
* add find job implementation (7cc7c3bcbb1f)
* add scheduler start to cmdline entry point (d30ded29ba1f)
* extend recipe to generate html view (e0f0c51065c1)
* add prototype of recipe to chain data procession (8667c4c3263d)

### Fix

* copy todo to testdir to avoid deleting todo source folder (8856bc3f85a5)
* publish to `result` folder which `viewo` expects (017fb277a87b)
* fix output of words index, which was doubled (291fbca59589)
* remove verbose flag to use it from utila (ceeb7dd02c58)
* use only folder which are not in progress (f0f1f6af0e49)
* fix logging of recipe (0fa0740e7eaa)
* fix spelling recipe (6f5f7c574d0f)
* extend imports to include every package of project (5989a2968b59)

### Documentation

* update strategy paper and include to main document (0a80233e14c6)

## v0.0.1

### Feature

* add external statistica and feedback module (388c162a5c22)
* add rawmaker and groupme feature packages (6982ae4c4a42)
* push job after finishing job to ready folder (df7745bbeaa7)
* limit loop by max ticks to avoid endless loop (29e223ac0877)
* using job definition from `link` (9cd6bc5dc5ec)
* add scheduler to watch todo folder and start working (1487e3580310)
* move access to global environment to configo package (7e0b50e46671)
* add access to config with todo and ready folder (2bc49534f5a4)

## v0.0.0 Initial release

