# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tax'
        db.create_table('django_price_tax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_poly_ct', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal('django_price', ['Tax'])

        # Adding model 'LinearTax'
        db.create_table('django_price_lineartax', (
            ('tax_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_price.Tax'], unique=True, primary_key=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=3)),
        ))
        db.send_create_signal('django_price', ['LinearTax'])

        # Adding model 'MultiTax'
        db.create_table('django_price_multitax', (
            ('tax_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_price.Tax'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('django_price', ['MultiTax'])

        # Adding M2M table for field taxes on 'MultiTax'
        db.create_table('django_price_multitax_taxes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('multitax', models.ForeignKey(orm['django_price.multitax'], null=False)),
            ('tax', models.ForeignKey(orm['django_price.tax'], null=False))
        ))
        db.create_unique('django_price_multitax_taxes', ['multitax_id', 'tax_id'])


    def backwards(self, orm):
        
        # Deleting model 'Tax'
        db.delete_table('django_price_tax')

        # Deleting model 'LinearTax'
        db.delete_table('django_price_lineartax')

        # Deleting model 'MultiTax'
        db.delete_table('django_price_multitax')

        # Removing M2M table for field taxes on 'MultiTax'
        db.delete_table('django_price_multitax_taxes')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_price.lineartax': {
            'Meta': {'object_name': 'LinearTax', '_ormbases': ['django_price.Tax']},
            'percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '3'}),
            'tax_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_price.Tax']", 'unique': 'True', 'primary_key': 'True'})
        },
        'django_price.multitax': {
            'Meta': {'object_name': 'MultiTax', '_ormbases': ['django_price.Tax']},
            'tax_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_price.Tax']", 'unique': 'True', 'primary_key': 'True'}),
            'taxes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['django_price.Tax']"})
        },
        'django_price.tax': {
            'Meta': {'object_name': 'Tax'},
            '_poly_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['django_price']
