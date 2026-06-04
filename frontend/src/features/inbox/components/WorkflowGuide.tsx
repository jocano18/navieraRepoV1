import { Card, CardBody } from '@/components/ui';

const STEPS = [
  { n: 1, title: 'Bandeja', text: 'PDFs nuevos del correo o carpeta compartida.' },
  { n: 2, title: 'Crear envío', text: 'Un PDF = un expediente. Indica HBL/MBL y tipo de carga.' },
  { n: 3, title: 'Extracción', text: 'El sistema lee el PDF (Operador).' },
  { n: 4, title: 'Digitación', text: 'El operador corrige/completa los campos del B/L.' },
  { n: 5, title: 'Validación', text: 'El ejecutivo compara PDF vs datos (pantalla dividida).' },
  { n: 6, title: 'Notificación', text: 'Si todo coincide, se aprueba y notifica al cliente.' },
];

export function WorkflowGuide() {
  return (
    <Card className="border-violet/30 bg-gradient-to-r from-lilac-soft to-surface">
      <CardBody>
        <h2 className="text-sm font-bold text-brand">¿Cómo funciona este sistema?</h2>
        <p className="mt-1 text-xs text-text-muted">
          Digitaliza conocimientos de embarque (B/L): cada envío sigue el mismo orden. HBL y MBL
          son tipos de documento; la carga directa o consolidada define cómo se extraen los datos.
        </p>
        <ol className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {STEPS.map((s) => (
            <li
              key={s.n}
              className="flex gap-3 rounded-lg border border-border bg-surface px-3 py-2 text-xs"
            >
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent text-[10px] font-bold text-white">
                {s.n}
              </span>
              <div>
                <p className="font-semibold text-brand">{s.title}</p>
                <p className="text-text-muted">{s.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </CardBody>
    </Card>
  );
}
