import js from '@eslint/js';
import importPlugin from 'eslint-plugin-import';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import globals from 'globals';
import tseslint from 'typescript-eslint';

const featureNames = ['dashboard', 'inbox', 'shipments', 'validation', 'notifications'];

const featureZones = featureNames.map((name) => ({
  target: `./src/features/${name}`,
  from: './src/features',
  except: [`./src/features/${name}`],
}));

export default tseslint.config(
  { ignores: ['dist', 'node_modules', 'coverage'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.strictTypeChecked],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: globals.browser,
      parserOptions: {
        project: ['./tsconfig.json', './tsconfig.node.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
      import: importPlugin,
    },
    settings: {
      'import/resolver': {
        typescript: {
          alwaysTryTypes: true,
          project: './tsconfig.json',
        },
      },
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
      'import/no-restricted-paths': [
        'error',
        {
          zones: [
            ...featureZones,
            {
              target: './src/components',
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/hooks',
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/lib',
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/utils',
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/types',
              from: ['./src/features', './src/app'],
            },
            {
              target: './src/stores',
              from: ['./src/features', './src/app'],
            },
          ],
        },
      ],
    },
  },
);
