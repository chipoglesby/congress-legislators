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


C_FILES = {
  'legislators' => DIRS['compiled'] / 'legislators.csv',
  'congresses' => DIRS['compiled'] / 'congresses.csv',
  'terms' => DIRS['compiled'] / 'terms.csv',
}


P_FILES = {
  'legislators' => DIRS['published'] / 'legislators.csv',
  'congresses' => DIRS['published'] / 'congresses.csv',
  'terms' => DIRS['published'] / 'terms.csv',
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

desc "Fetch everything"
task :fetch  => [:setup] do
  F_FILES.each_value{|fn| Rake::Task[fn].execute() }
end

desc "Compile everything"
task :compile  => [:setup] do
  C_FILES.each_value{|fn| Rake::Task[fn].execute() }
end

desc "Publish everything"
task :publish  => C_FILES.values() do
  C_FILES.each_value do |fn|
    sh %Q{
cp #{fn} #{DIRS['published'] / fn.basename}
    }
  end
end



namespace :files do
  namespace :published do
      SOURCE_URLPATH = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master'


      file C_FILES['legislators'] => [F_FILES['legislators-current'],
                                      F_FILES['legislators-historical']] do

        sh %Q{
python #{SCRIPTS / 'collate_legislators.py'} \
  #{F_FILES['legislators-current']} \
  #{F_FILES['legislators-historical']} \
> #{C_FILES['legislators']}
        }
      end


      desc "The file containing congress and numbers"
      file C_FILES['congresses'] => F_FILES['sessions'] do
        sh %Q{
python #{SCRIPTS / 'collate_congresses.py'} \
  #{F_FILES['sessions']} \
  > #{C_FILES['congresses']}
          }
      end


      file C_FILES['terms'] => [F_FILES['legislators-current'],
                                      F_FILES['legislators-historical']] do

        sh %Q{
python #{SCRIPTS / 'collate_terms.py'} \
  #{F_FILES['legislators-current']} \
  #{F_FILES['legislators-historical']} \
> #{C_FILES['terms']}
        }
      end
  end


  namespace :fetched do
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
end
