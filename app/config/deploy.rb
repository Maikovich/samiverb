set :application, "Samiverb"
set :domain,      "samiverb.com"
set :deploy_to,   "/home/maikovich/www"

set :use_sudo,      false
set :user, "maikovich"

set :repository,  "git@github.com:Maikovich/samiverb.git"
set :scm,         :git
# Or: `accurev`, `bzr`, `cvs`, `darcs`, `subversion`, `mercurial`, `perforce`, or `none`

set :model_manager, "doctrine"
# Or: `propel`

role :web,        domain                         # Your HTTP server, Apache/etc
role :app,        domain, :primary => true       # This may be the same as your `Web` server

set  :keep_releases,  3

set :shared_files,      ["app/config/parameters.yml"]
set :shared_children,     [app_path + "/logs", web_path + "/uploads", "vendor"]
set :use_composer, true
set :update_vendors, true

set :writable_dirs,       ["app/cache", "app/logs", "app/sessions"]

logger.level = Logger::MAX_LEVEL

default_run_options[:pty] = true

ssh_options[:forward_agent] = true
# Be more verbose by uncommenting the following line
# logger.level = Logger::MAX_LEVEL