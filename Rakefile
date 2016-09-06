require 'pathname'
DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS = WRANGLE_DIR.join('scripts')
DIRS = {
    'fetched' => CORRAL_DIR / 'fetched',
    'compiled' => CORRAL_DIR / 'compiled',
    'published' => DATA_DIR,
}

F_FILES = {
  'sessions' => DIRS['fetched'] / 'sessions.tsv',
  'legislators-current' => DIRS['fetched'] / 'legislators-current.yaml',
  'legislators-historical' => DIRS['fetched'] / 'legislators-historical.yaml',
}


desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end

namespace :publish do
  desc "Fetch legislators YAML and sessions"
  task :fetch do
    F_FILES.each_value{|fn| Rake::Task[fn].execute() }
  end
end


namespace :files do
  SOURCE_URLPATH = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master'


  file F_FILES['sessions'] do
    sh %Q{
          curl https://www.govtrack.us/data/us/sessions.tsv \
          -o #{F_FILES['sessions']}
        }
  end

  file F_FILES['legislators-current'] do
    sh %Q{
          curl #{SOURCE_URLPATH}/legislators-current.yaml \
          -o #{F_FILES['legislators-current']}
        }
  end

  file F_FILES['legislators-historical'] do
    sh %Q{
          curl #{SOURCE_URLPATH}/legislators-historical.yaml \
          -o #{F_FILES['legislators-historical']}
        }
  end

end
