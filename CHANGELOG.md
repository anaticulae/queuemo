# Changelog

Every noteable change is logged here.

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

