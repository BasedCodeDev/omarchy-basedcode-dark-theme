-- Exercise the installed Aether plugin against the generated palette, without user plugins.
local root = assert(os.getenv('BASEDCODE_ROOT'))
vim.opt.runtimepath:append(vim.fn.expand('~/.local/share/nvim/lazy/aether'))
local spec = dofile(root .. '/build/generated/neovim.lua')
require('aether').setup(spec[1].opts)
vim.cmd.colorscheme('aether')
local result = {}
for _, name in ipairs({'Normal','Comment','Visual','Search','IncSearch','DiffAdd','DiffDelete','DiffChange','DiagnosticError','DiagnosticWarn','DiagnosticInfo','DiagnosticHint'}) do
  result[name] = vim.api.nvim_get_hl(0, {name=name,link=false})
end
vim.fn.writefile({vim.json.encode(result)},root .. '/qa/nvim-highlights.json')
vim.cmd('qa!')
