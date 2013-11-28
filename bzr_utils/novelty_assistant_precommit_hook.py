import bzrlib.branch

def pre_commit_hook(local, master, old_revno, old_revid, future_revno, future_revid, tree_delta, future_tree):
	path = master._get_base().replace("file://", "")
	if path.find("novelty_assistant") != -1:
		file_name = "%sconstants.py" % path
		fr = open(file_name, 'r')
		
		restart = False
		new_lines = []
		for line in fr:
			if line.find("PROGRAM_REVISION_NUMBER = ") > -1:
				beg = line.find("'")
				end = line.find("'", beg + 1)
				if (beg != -1) and (end != -1):
					current_revno = line[beg + 1 : end]
					if str(current_revno) != str(future_revno):
						restart = True
				line = "PROGRAM_REVISION_NUMBER = '%s'\n" % future_revno
			new_lines += line
		fr.close()

		fw = open(file_name, 'w')
		fw.writelines(new_lines)
		fw.close()

		if restart:
			raise Exception("File version updated. Restart commit operation.")

bzrlib.branch.Branch.hooks.install_named_hook('pre_commit', pre_commit_hook, 'Novelty Assistant version setter')